"""
core/wms_utils.py — Funciones utilitarias vectorizadas para transformación de datos WMS.
"""
import re
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Final

from core.wms_config import STATUS_MAPPING, COST_CENTER_MAPPING
from core.db_config_manager import get_holidays
from sqlalchemy.orm import Session
from sqlalchemy import text

# Configuración de Logging
logger = logging.getLogger("wms-utils")

# ─── EXPRESIONES REGULARES COMPILADAS ─────────────────────────────────────────
# Compilar una vez a nivel de módulo para máximo rendimiento
RE_CLEAN: Final = re.compile(r'[\s\-\.]+')
RE_UNSAFE: Final = re.compile(r'[^a-zA-Z0-9_]')
RE_DATE_DOT: Final = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')

# ─── LIMPIEZA DE DATOS (CLEANING) ─────────────────────────────────────────────

def sanitize_string(text: str) -> str:
    """
    Normaliza un string para usarlo como encabezado de columna (snake_case).
    Determinista: no utiliza números aleatorios.
    """
    if not isinstance(text, str):
        if pd.isna(text):
            return "unnamed_column"
        text = str(text)
    
    text = text.strip()
    text = RE_CLEAN.sub('_', text)
    text = RE_UNSAFE.sub('', text)
    name = text.lower()
    
    # Mapeo de alias técnicos a nombres de dominio (Agnóstico)
    aliases = {
        # Fechas
        'sal_mcas_': 'fecha_sm_real',
        'fe_sm_real': 'fecha_sm_real',
        'fecha_sm_real': 'fecha_sm_real',
        'fe_carga': 'fecha_carga',
        'fecha_carga': 'fecha_carga',
        'creado_el': 'creado_el',
        
        # Cantidades
        'ctdentrega': 'cantidad',
        'cantidad_entrega': 'cantidad',
        'ctd_entrega': 'cantidad',
        
        # Ubicaciones
        'ubicacion': 'ubicacion_bin',
        'ubicacin': 'ubicacion_bin',
        'ubicacin_1': 'ubicacion_area',
        'ubicacion_1': 'ubicacion_area',
        'ubicacion_fisica_stock': 'ubicacion_bin',
        
        # Otros
        'estado_sap': 'estado_wms',
        'centro_costo': 'centro_costo',
        'ce_coste': 'centro_costo',
        'denominacion': 'denominacion',
        'texto_breve_de_material': 'denominacion',
        'texto_breve_material': 'denominacion',
        'texto_breve_de_mat': 'denominacion'
    }
    return aliases.get(name, name)

# ─── MAPEOS DE NEGOCIO (MAPPING) ─────────────────────────────────────────────

def map_wms_status(df: pd.DataFrame) -> pd.DataFrame:
    """Concatena columnas de estado y mapea al valor legible de negocio."""
    cols_needed = ['ops', 'c', 'mm']
    if all(col in df.columns for col in cols_needed):
        # Operación vectorizada de concatenación
        concat_key = (
            df['ops'].fillna('').astype(str).str.strip() +
            df['c'].fillna('').astype(str).str.strip() +
            df['mm'].fillna('').astype(str).str.strip()
        )
        df['estado_wms'] = concat_key.map(STATUS_MAPPING).fillna("Desconocido")
        logger.debug("Mapeo de estados WMS completado.")
    return df

def apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
    Sustituye el uso de .apply() por una lógica de mapeo más rápida.
    """
    if 'centro_costo' not in df.columns:
        return df

    # Inicializar con el valor por defecto
    df['area_negocio'] = 'OTRO'
    
    # Aplicar mapeos en orden (vectorizado)
    # Convertimos la columna a UPPER una sola vez
    ubi_upper = df['centro_costo'].fillna('').astype(str).str.upper()
    
    for prefix, area in COST_CENTER_MAPPING.items():
        # Buscamos el prefijo en la ubicación
        mask = ubi_upper.str.contains(prefix, regex=False)
        df.loc[mask, 'area_negocio'] = area
        
    logger.debug("Mapeo de áreas de negocio (Centros de Costo) completado.")
    return df

# ─── NORMALIZACIÓN Y MÉTRICAS (METRICS) ───────────────────────────────────────

def normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente."""
    for col in df.columns:
        # Tomar una muestra no nula
        non_null = df[col].dropna()
        if non_null.empty:
            continue
            
        sample = non_null.iloc[0]
        
        # Caso 1: String con puntos (dd.mm.yyyy)
        if isinstance(sample, str) and RE_DATE_DOT.match(sample):
            df[col] = df[col].str.replace('.', '-', regex=False)
        # Caso 2: Objeto datetime/timestamp
        elif isinstance(sample, (pd.Timestamp, datetime)):
            df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%m-%Y')
            
    return df

def calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula días hábiles de retraso usando lógica vectorizada de NumPy."""
    if 'creado_el' not in df.columns or 'fecha_sm_real' not in df.columns:
        return df


    # Conversión eficiente a datetime
    s_date = pd.to_datetime(df['creado_el'], format='%d-%m-%Y', errors='coerce')
    e_date = pd.to_datetime(df['fecha_sm_real'], format='%d-%m-%Y', errors='coerce')
    
    valid = s_date.notna() & e_date.notna()
    df['dias_retraso'] = np.nan
    
    if valid.any():
        # Cálculo de días hábiles (Business Days) con NumPy
        s_values = s_date[valid].values.astype('datetime64[D]')
        e_values = e_date[valid].values.astype('datetime64[D]')
        
        # Normalizar fechas al siguiente día hábil si caen en fin de semana o festivo
        holidays_list = get_holidays()
        s_bus = np.busday_offset(s_values, 0, roll='forward', holidays=holidays_list)
        e_bus = np.busday_offset(e_values, 0, roll='forward', holidays=holidays_list)
        
        df.loc[valid, 'dias_retraso'] = np.maximum(0, np.busday_count(s_bus, e_bus, holidays=holidays_list))
    
    return df

def generate_time_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Genera etiquetas de semana ISO para visualización y analítica."""
    # Prioridad de columnas para determinar la fecha de referencia
    date_cols = ['fecha_carga', 'fecha_sm_real', 'creado_el']
    ref_date = pd.Series(index=df.index, dtype='object')
    
    for col in date_cols:
        if col in df.columns:
            # Reemplazar vacíos por NA y combinar
            ref_date = ref_date.combine_first(df[col].replace('', pd.NA))
    
    temp_date = pd.to_datetime(ref_date, format='%d-%m-%Y', errors='coerce')
    valid = temp_date.notna()
    
    df['week_sort'] = None
    df['week_label'] = None
    
    if valid.any():
        v_dates = temp_date[valid]
        df.loc[valid, 'week_sort'] = v_dates.dt.strftime('%Y-%V')
        
        meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
        
        month_name = v_dates.dt.month.map(meses)
        week_num = v_dates.dt.isocalendar().week.astype(str).str.zfill(2)
        df.loc[valid, 'week_label'] = month_name + "-S" + week_num
        
    return df


def _manifest_execute(session_or_conn, sql: str, params: dict):
    """
    Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
    Centraliza la diferencia de API entre ambos tipos de conexión.
    """
    from sqlalchemy.orm import Session as SASession
    if isinstance(session_or_conn, SASession):
        # SQLAlchemy Session → usa text() y dict nombrado
        return session_or_conn.execute(text(sql), params)
    else:
        # sqlite3.Connection → convierte a ? posicional
        # Los params del manifiesto siempre tienen las mismas claves, mapeamos en orden
        import re as _re
        positional_sql = _re.sub(r':\w+', '?', sql)
        ordered_values = list(params.values())
        return session_or_conn.execute(positional_sql, ordered_values)


def is_file_changed(session_or_conn, file_path: Path) -> bool:
    """
    Verifica si un archivo ha cambiado desde la última sincronización.
    Acepta SQLAlchemy Session o sqlite3.Connection.
    Retorna True si el archivo es nuevo o ha sido modificado (mtime/size).
    """
    if not file_path.exists():
        return False

    try:
        stats    = file_path.stat()
        mtime    = stats.st_mtime
        size     = stats.st_size
        path_str = str(file_path.absolute())

        result = _manifest_execute(
            session_or_conn,
            "SELECT last_modified, file_size FROM sync_manifest WHERE file_path = :path",
            {"path": path_str}
        )
        row = result.fetchone()

        if row:
            db_mtime, db_size = row
            if db_mtime == mtime and db_size == size:
                logger.debug(f"Archivo sin cambios detectados: {file_path.name} ({size} bytes)")
                return False
            logger.info(f"Cambio detectado en {file_path.name}: "
                        f"Size {db_size} -> {size}, MTime {db_mtime} -> {mtime}")

        return True
    except Exception as e:
        logger.error(f"Error verificando manifiesto para {file_path.name}: {e}")
        return True  # Por seguridad, si falla asumimos que cambió


def mark_file_processed(session_or_conn, file_path: Path, row_count: Optional[int] = None):
    """Marca un archivo como procesado en el manifiesto.
    Acepta SQLAlchemy Session o sqlite3.Connection."""
    try:
        stats    = file_path.stat()
        mtime    = stats.st_mtime
        size     = stats.st_size
        path_str = str(file_path.absolute())
        now      = datetime.now().isoformat()

        # Asegurar que la columna row_count existe
        try:
            _manifest_execute(session_or_conn, "ALTER TABLE sync_manifest ADD COLUMN row_count INTEGER", {})
        except Exception:
            pass  # Ya existe

        _manifest_execute(session_or_conn, """
            INSERT INTO sync_manifest (file_path, last_modified, file_size, processed_at, row_count)
            VALUES (:path, :mtime, :size, :now, :row_count)
            ON CONFLICT(file_path) DO UPDATE SET
                last_modified = excluded.last_modified,
                file_size     = excluded.file_size,
                processed_at  = excluded.processed_at,
                row_count     = COALESCE(excluded.row_count, sync_manifest.row_count)
        """, {"path": path_str, "mtime": mtime, "size": size, "now": now, "row_count": row_count})

        # Commit según tipo de conexión
        from sqlalchemy.orm import Session as SASession
        if isinstance(session_or_conn, SASession):
            session_or_conn.commit()
        else:
            session_or_conn.commit()

    except Exception as e:
        logger.error(f"Error actualizando manifiesto para {file_path.name}: {e}")
