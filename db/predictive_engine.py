import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from itertools import combinations
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wms_config import COST_CENTER_MAPPING, get_query

logger = logging.getLogger(__name__)

def generate_predictions(db_path: str):
    """
    Procesa Movimientos Transactions para generar modelos predictivos:
    1. Market Basket Analysis (Combos)
    2. Frecuencia vs Volumen (Corredores vs Elefantes)
    3. MTBV y Semáforo de Desplanificación
    """
    try:
        conn = sqlite3.connect(db_path)
        
        # Leemos la data base de consumos reales
        query_db = get_query("ia_predictive_movements")
        query = query_db if query_db else """
            SELECT 
                fe_contab, ce_coste, material, texto_breve_material, cantidad, cmv
            FROM inventory_movements 
            WHERE cmv IN ('201', '261') AND length(fe_contab) >= 10
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            return {"error": "No hay data suficiente para el motor predictivo."}

        # 0. Limpieza y Parseo de Fechas
        def parse_date(date_str):
            try:
                # Assuming format DD.MM.YYYY
                parts = date_str.split('.')
                if len(parts) == 3:
                    return pd.to_datetime(f"{parts[2]}-{parts[1]}-{parts[0]}")
                # Try DD-MM-YYYY
                parts = date_str.split('-')
                if len(parts) == 3:
                    return pd.to_datetime(f"{parts[2]}-{parts[1]}-{parts[0]}")
                return pd.NaT
            except:
                return pd.NaT

        df['date'] = df['fe_contab'].apply(parse_date)
        df = df.dropna(subset=['date'])
        
        if df.empty:
            return {"error": "Fallo en el parseo de fechas de Movimientos."}

        df['dow'] = df['date'].dt.dayofweek # 0=Monday, 6=Sunday
        df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0).abs()
        df['mat_full'] = "[" + df['material'].astype(str) + "] " + df['texto_breve_material']
        
        def map_area(ce):
            if pd.isna(ce) or not str(ce).strip(): return 'OTRO'
            ce_str = str(ce).upper()
            for code, name in COST_CENTER_MAPPING.items():
                if code in ce_str:
                    return name
            return ce_str
            
        df['ce_coste'] = df['ce_coste'].apply(map_area)
        
        # Crear diccionarios de resultados
        results = {
            "combos": [],
            "scatter_data": [],
            "alerts": []
        }

        # ==========================================
        # 1. Market Basket Analysis (Correlaciones)
        # ==========================================
        # Agrupamos por fecha (fecontab) para ver qué se pide junto en el mismo día.
        # Filtramos materiales muy poco frecuentes para no generar ruido.
        mat_counts = df['mat_full'].value_counts()
        valid_mats = mat_counts[mat_counts > 10].index.tolist()
        
        basket_df = df[df['mat_full'].isin(valid_mats)]
        # Rellenamos nulos para que no rompa el group_by
        basket_df['ce_coste'] = basket_df['ce_coste'].fillna('Desconocida')
        baskets = basket_df.groupby(['date', 'ce_coste'])['mat_full'].apply(set).tolist()
        
        combo_counts = Counter()
        for basket in baskets:
            if len(basket) > 1:
                # Contamos todas las parejas posibles dentro de un mismo día
                for combo in combinations(sorted(basket), 2):
                    combo_counts[combo] += 1
                    
        # Tomamos los top 15 combos más repetidos
        top_combos = combo_counts.most_common(100)
        for combo, count in top_combos:
            mat_a, mat_b = combo
            # Probabilidad simple: (veces juntos) / (veces que A aparece solo)
            count_a = mat_counts.get(mat_a, 1)
            prob = (count / count_a) * 100
            # Si prob > 100 por alguna razón matemática rara, lo limitamos
            prob = min(prob, 99.9)
            
            results["combos"].append({
                "mat_a": mat_a,
                "mat_b": mat_b,
                "count": count,
                "probability_num": prob,
                "probability": f"{prob:.1f}%"
            })
            
        # Ordenamos los combos por mayor probabilidad
        results["combos"] = sorted(results["combos"], key=lambda x: x["probability_num"], reverse=True)


        # ==========================================
        # 2. Frecuencia vs Volumen (Corredores vs Elefantes)
        # ==========================================
        # Agrupamos por material
        mat_stats = df.groupby(['material', 'texto_breve_material']).agg(
            frecuencia=('date', 'count'),
            volumen_total=('cantidad', 'sum')
        ).reset_index()
        
        # Filtramos anomalías estadísticas extremas (ruido) o cosas que se pidieron 1 sola vez
        mat_stats = mat_stats[mat_stats['frecuencia'] > 1]
        
        # Promedio por despacho
        mat_stats['volumen_promedio'] = mat_stats['volumen_total'] / mat_stats['frecuencia']
        
        # Categorización Simple basada en Cuartiles
        # Frecuencia Alta = Corredor. Volumen Alto, Freq Baja = Elefante.
        freq_median = mat_stats['frecuencia'].median()
        vol_median = mat_stats['volumen_promedio'].median()
        
        def classify_mat(row):
            if row['frecuencia'] >= freq_median and row['volumen_promedio'] <= vol_median:
                return "Corredor"
            elif row['frecuencia'] < freq_median and row['volumen_promedio'] > vol_median:
                return "Elefante"
            elif row['frecuencia'] >= freq_median and row['volumen_promedio'] > vol_median:
                return "Crítico"
            else:
                return "Tortuga"
                
        mat_stats['categoria'] = mat_stats.apply(classify_mat, axis=1)
        
        # Solo enviaremos una muestra representativa al scatter plot (top 150)
        # para no saturar el navegador con 5000 puntos
        scatter_sample = mat_stats.sort_values(by='frecuencia', ascending=False).head(200)
        
        today = df['date'].max() # Usamos el "hoy" relativo al último dato en la BD
        if pd.isna(today):
            today = datetime.now()
        current_year = today.year
        current_month = today.month
        
        for _, row in scatter_sample.iterrows():
            mat_df = df[df['material'] == row['material']]
            area_counts = mat_df['ce_coste'].value_counts()
            
            if area_counts.empty:
                continue
            else:
                for area, count in area_counts.items():
                    if pd.isna(area): continue
                    
                    area_df = mat_df[mat_df['ce_coste'] == area]
                    # Datos del mes actual para esta area
                    mat_df_curr = area_df[(area_df['date'].dt.year == current_year) & (area_df['date'].dt.month == current_month)]
                    curr_freq = len(mat_df_curr)
                    curr_vol = mat_df_curr['cantidad'].sum()
                    curr_month_str = f"{curr_freq} retiros ({int(curr_vol)} unds)"
                    
                    vol_promedio_area = area_df['cantidad'].sum() / count if count > 0 else 0

                    results["scatter_data"].append({
                        "x": int(count), # Frecuencia especifica de esta area
                        "y": float(round(vol_promedio_area, 2)), # Volumen prom de esta area
                        "name": f"[{row['material']}] {row['texto_breve_material']}",
                        "category": row['categoria'],
                        "area": str(area),
                        "area_clean": str(area),
                        "curr_month": curr_month_str
                    })

        # ==========================================
        # 3. MTBV, Estacionalidad DOW y Semáforo de Desplanificación
        # ==========================================
        alerts = []

        # Calculamos la estacionalidad general (DOW Bias)
        # Qué porcentaje del volumen total sale cada día
        dow_counts = df['dow'].value_counts(normalize=True).to_dict()
        
        # Analizaremos los "Fast Movers" para las alertas (frecuencia > 5)
        fast_movers = mat_stats[mat_stats['frecuencia'] >= 5].copy()
        # Creamos una columna 'mat_full' en mat_stats para igualar
        fast_movers['mat_full'] = "[" + fast_movers['material'].astype(str) + "] " + fast_movers['texto_breve_material']
        fast_movers_list = fast_movers['mat_full'].tolist()
        
        for mat in fast_movers_list[:200]: # Limitamos a los top 200 para rendimiento
            mat_df_full = df[df['mat_full'] == mat]
            
            for area, mat_df in mat_df_full.groupby('ce_coste'):
                if len(mat_df) < 3:
                    continue # Necesitamos al menos 3 retiros de ESTA área para hacer un patrón
                    
                mat_df = mat_df.sort_values('date')
                
                # Calcular los días entre pedidos (MTBV) para esta área específica
                mat_df['days_diff'] = mat_df['date'].diff().dt.days
                
                avg_interval = mat_df['days_diff'].mean()
                std_interval = mat_df['days_diff'].std()
                avg_qty = mat_df['cantidad'].mean()
                
                if pd.isna(avg_interval) or pd.isna(std_interval):
                    continue
                    
                last_date = mat_df['date'].max()
                days_since = (today - last_date).days
                
                # Semáforo
                comportamiento = "Estable" if std_interval < (avg_interval * 0.6) else "Errático"
                
                score = 0
                if days_since >= avg_interval:
                    retraso = days_since - avg_interval
                    tomorrow_dow = (today.dayofweek + 1) % 7
                    dow_bonus = dow_counts.get(tomorrow_dow, 0) * 100 
                    
                    base_score = min(50 + (retraso * 5), 90) 
                    score = base_score + (dow_bonus * 0.5)
                    score = min(score, 99.9)
                    
                if score > 50:
                    # Datos del mes actual para esta alerta de área
                    mat_df_curr = mat_df[(mat_df['date'].dt.year == current_year) & (mat_df['date'].dt.month == current_month)]
                    curr_freq = len(mat_df_curr)
                    curr_vol = mat_df_curr['cantidad'].sum()
                    curr_month_str = f"{curr_freq} retiros ({int(curr_vol)} unds)"

                    color = "danger" if score > 85 else "warning"
                    alerts.append({
                        "material": mat,
                        "area": str(area) if pd.notna(area) else "Área Desconocida",
                        "avg_interval": round(avg_interval, 1),
                        "days_since": int(days_since),
                        "avg_qty": round(avg_qty, 1),
                        "curr_month": curr_month_str,
                        "score": round(score, 1),
                        "behavior": comportamiento,
                        "color": color
                    })
                
        # Ordenar alertas por intervalo promedio
        alerts = sorted(alerts, key=lambda x: x['avg_interval'])
        results["alerts"] = alerts[:300] # Subimos a 300 porque ahora hay múltiples alertas por material

        return results
        
    except Exception as e:
        logger.error(f"Error en predictive_engine: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import os
    # Test
    db = os.path.join(os.path.dirname(__file__), "../wms_transactions.db")
    res = generate_predictions(db)
    print("Combos:", len(res.get("combos", [])))
    print("Scatter:", len(res.get("scatter_data", [])))
    print("Alertas:", len(res.get("alerts", [])))
