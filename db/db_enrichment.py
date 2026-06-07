"""
db_enrichment.py — Enriquecimiento de datos mediante SQL atómico y seguro.
"""
import logging
import sqlite3
from typing import Final, List

import pandas as pd

from core.security import validate_table

logger = logging.getLogger("db-enrichment")

def backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements"):
    """
    Rellena columnas vacías en Entregas (autor, ubicacion, textos) cruzando con Movimientos.
    Utiliza SQL directo para evitar la destrucción de la tabla original.
    """
    validate_table(trans_table)
    validate_table(movements_table)

    logger.info(f"Iniciando backfill de {trans_table} desde {movements_table}...")

    try:
        # 1. Extraer datos necesarios de Movimientos para inferencia
        # Solo extraemos registros con referencia para el cruce
        movements_query = f"""
            SELECT material, usuario, ce_coste, texto_breve_material as txt_movements, referencia
            FROM {movements_table}
            WHERE referencia IS NOT NULL AND referencia != ''
        """
        movements_df = pd.read_sql(movements_query, conn)

        if movements_df.empty:
            logger.warning("No hay datos en Movimientos para realizar el cruce.")
            return

        # Normalizar para el cruce (limpiar ceros a la izquierda)
        movements_df['entrega_match'] = movements_df['referencia'].str.extract(r'(\d+)')[0].fillna('').str.lstrip('0')

        # Agrupar para obtener el autor y centro de costo más probable por entrega
        lookup = movements_df.groupby('entrega_match').agg({
            'usuario': 'first',
            'ce_coste': 'first',
            'txt_movements': 'first'
        }).reset_index()

        # 2. Actualizar mediante tabla temporal para no destruir la principal
        with conn:
            # Crear tabla temporal de mapeo
            lookup.to_sql("tmp_backfill_map", conn, if_exists='replace', index=False)

            # Actualizar AUTOR donde esté vacío
            conn.execute(f"""
                UPDATE {trans_table}
                SET autor = (SELECT usuario FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
                WHERE (autor IS NULL OR autor = '')
                AND EXISTS (SELECT 1 FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
            """)

            # Actualizar UBICACIÓN donde esté vacía
            conn.execute(f"""
                UPDATE {trans_table}
                SET centro_costo = (SELECT ce_coste FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
                WHERE (centro_costo IS NULL OR centro_costo = '')
                AND EXISTS (SELECT 1 FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
            """)

            # Actualizar TEXTO DE MATERIAL donde esté vacío
            conn.execute(f"""
                UPDATE {trans_table}
                SET denominacion = (SELECT txt_movements FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
                WHERE (denominacion IS NULL OR denominacion = '')
                AND EXISTS (SELECT 1 FROM tmp_backfill_map WHERE entrega_match = ltrim(CAST({trans_table}.entrega AS TEXT), '0'))
            """)

            conn.execute("DROP TABLE IF EXISTS tmp_backfill_map")

        logger.info("Backfill desde Movimientos completado exitosamente.")

    except Exception as e:
        logger.error(f"Fallo en backfill_deliveries_from_movements: {e}")

def learn_author_areas(conn: sqlite3.Connection):
    """Actualiza el mapeo de frecuencia Autor -> Área."""
    logger.info("Actualizando memoria de autores (Autor -> Área)...")
    try:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS autor_area_mapping (
                    autor        TEXT,
                    area_negocio TEXT,
                    frequency    INTEGER,
                    PRIMARY KEY (autor, area_negocio)
                )
            ''')
            conn.execute('''
                INSERT OR REPLACE INTO autor_area_mapping (autor, area_negocio, frequency)
                SELECT autor, area_negocio, COUNT(*) AS frequency
                FROM outbound_deliveries
                WHERE area_negocio != 'OTRO' AND autor IS NOT NULL AND autor != ''
                GROUP BY autor, area_negocio
            ''')
    except sqlite3.Error as e:
        logger.error(f"Error en learn_author_areas: {e}")

def apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries"):
    """Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor."""
    validate_table(table_name)
    logger.info(f"Aplicando memoria de autores a transacciones sin área en {table_name}...")
    try:
        with conn:
            conn.execute(f'''
                UPDATE {table_name}
                SET area_negocio = (
                    SELECT a.area_negocio
                    FROM autor_area_mapping a
                    WHERE a.autor = {table_name}.autor
                    ORDER BY a.frequency DESC
                    LIMIT 1
                )
                WHERE area_negocio = 'OTRO'
                  AND autor IN (SELECT autor FROM autor_area_mapping)
            ''')
            logger.info(f"Corrección de áreas completada (Filas afectadas: {conn.total_changes})")
    except Exception as e:
        logger.error(f"Error en apply_author_learning: {e}")

def enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels"):
    """Enriquece transacciones con descripciones y ubicaciones físicas de Stock."""
    validate_table(trans_table)
    validate_table(stock_table)

    logger.info(f"Enriqueciendo {trans_table} con datos de stock de {stock_table}...")

    try:
        # 1. Obtener la ubicación maestra (con más stock) para cada material
        # Detectar dinámicamente las columnas debido a sanitización
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({stock_table})")
        existing_cols = {row[1] for row in cursor.fetchall()}
        ubi_col = "ubicacion_bin" if "ubicacion_bin" in existing_cols else ("ubicacin" if "ubicacin" in existing_cols else "ubicacion")
        if "denominacion" in existing_cols:
            desc_col = "denominacion"
        elif "Texto breve de material" in existing_cols:
            desc_col = '"Texto breve de material"'
        else:
            desc_col = "texto_breve_de_material"

        mat_col = '"Material"' if "Material" in existing_cols else "material"
        umb_col = '"UMB"' if "UMB" in existing_cols else "umb"
        stock_col = '"Stock disp"' if "Stock disp" in existing_cols else "stock_disp"

        stock_query = f"SELECT {mat_col} as material, {desc_col} as texto_breve_de_material, {ubi_col} as ubicacion, {stock_col} as stock_disp, {umb_col} as umb FROM {stock_table}"
        stock_df = pd.read_sql(stock_query, conn)

        if stock_df.empty:
            logger.warning("Tabla de stock vacía. Saltando enriquecimiento.")
            return

        # Normalizar stock y obtener registro 'primary' por material
        stock_df['stock_num'] = pd.to_numeric(stock_df['stock_disp'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        primary = stock_df.sort_values(['material', 'stock_num'], ascending=[True, False]).drop_duplicates('material')

        # Preparar para cruce
        primary['mat_match'] = primary['material'].astype(str).str.strip().str.lstrip('0')
        mapping = primary[['mat_match', 'texto_breve_de_material', 'ubicacion', 'umb']]
        mapping.columns = ['mat_match', 'txt', 'ubi', 'umb']

        # 2. Actualizar mediante SQL atómico
        with conn:
            mapping.to_sql("tmp_stock_map", conn, if_exists='replace', index=False)

            # Actualizamos descripción, ubicación física y UMB
            conn.execute(f"""
                UPDATE {trans_table}
                SET
                    denominacion = (SELECT txt FROM tmp_stock_map WHERE mat_match = ltrim(CAST({trans_table}.material AS TEXT), '0')),
                    ubicacion_bin = (SELECT ubi FROM tmp_stock_map WHERE mat_match = ltrim(CAST({trans_table}.material AS TEXT), '0')),
                    umb = (SELECT umb FROM tmp_stock_map WHERE mat_match = ltrim(CAST({trans_table}.material AS TEXT), '0'))
                WHERE EXISTS (SELECT 1 FROM tmp_stock_map WHERE mat_match = ltrim(CAST({trans_table}.material AS TEXT), '0'))
            """)

            conn.execute("DROP TABLE IF EXISTS tmp_stock_map")

        logger.info("Enriquecimiento de stock completado exitosamente.")
    except Exception as e:
        logger.error(f"Error en enrich_deliveries_with_stock: {e}")

def backfill_material_texts(conn: sqlite3.Connection):
    """
    Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
    Esto soluciona el problema de materiales sin descripción en los reportes PDF.
    """
    logger.info("Rellenando descripciones de materiales faltantes desde todas las fuentes...")

    try:
        # 1. Extraer mapeos de todas las fuentes disponibles
        # De Stock (Fuente primaria: stock actual)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(stock_levels)")
        stock_cols = {row[1] for row in cursor.fetchall()}
        if "denominacion" in stock_cols:
            desc_col = "denominacion"
        elif "Texto breve de material" in stock_cols:
            desc_col = '"Texto breve de material"'
        else:
            desc_col = "texto_breve_de_material"

        mat_col = '"Material"' if "Material" in stock_cols else "material"
        umb_col = '"UMB"' if "UMB" in stock_cols else "umb"

        stock_df = pd.read_sql(f"""
            SELECT DISTINCT {mat_col} as material, {desc_col} as texto_breve_de_material, {umb_col} as umb
            FROM stock_levels
            WHERE {desc_col} IS NOT NULL AND {desc_col} != ''
        """, conn)
        stock_df['mat_match'] = stock_df['material'].astype(str).str.strip().str.lstrip('0')

        # De Movimientos (Fuente secundaria: historial de movimientos)
        movements_df = pd.read_sql("""
            SELECT DISTINCT material, texto_breve_material as texto, umb
            FROM inventory_movements
            WHERE texto_breve_material IS NOT NULL AND texto_breve_material != ''
        """, conn)
        movements_df['mat_match'] = movements_df['material'].astype(str).str.strip().str.lstrip('0')

        # 2. Consolidar: Prioridad Stock, luego Movimientos
        master_map = pd.concat([
            stock_df[['mat_match', 'texto_breve_de_material', 'umb']],
            movements_df.rename(columns={'texto': 'texto_breve_de_material'})[['mat_match', 'texto_breve_de_material', 'umb']]
        ]).drop_duplicates(subset=['mat_match'], keep='first')

        if master_map.empty:
            logger.warning("No se encontraron fuentes para backfill de textos.")
            return

        # 3. Aplicar mediante SQL atómico
        with conn:
            master_map.to_sql("tmp_text_backfill", conn, if_exists='replace', index=False)

            # Actualizar Descripciones vacías
            conn.execute("""
                UPDATE outbound_deliveries
                SET denominacion = (
                    SELECT texto_breve_de_material FROM tmp_text_backfill
                    WHERE mat_match = ltrim(CAST(outbound_deliveries.material AS TEXT), '0')
                )
                WHERE (denominacion IS NULL OR denominacion = '')
                AND EXISTS (
                    SELECT 1 FROM tmp_text_backfill
                    WHERE mat_match = ltrim(CAST(outbound_deliveries.material AS TEXT), '0')
                )
            """)

            # Actualizar UMB vacías
            conn.execute("""
                UPDATE outbound_deliveries
                SET umb = (
                    SELECT umb FROM tmp_text_backfill
                    WHERE mat_match = ltrim(CAST(outbound_deliveries.material AS TEXT), '0')
                )
                WHERE (umb IS NULL OR umb = '')
                AND EXISTS (
                    SELECT 1 FROM tmp_text_backfill
                    WHERE mat_match = ltrim(CAST(outbound_deliveries.material AS TEXT), '0')
                    AND umb != ''
                )
            """)

            conn.execute("DROP TABLE IF EXISTS tmp_text_backfill")

        logger.info("Backfill de descripciones completado.")

    except Exception as e:
        logger.error(f"Fallo en backfill_material_texts: {e}")

def update_sla_with_tasks(conn: sqlite3.Connection):
    """
    Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.
    """
    import numpy as np

    from core.db_config_manager import get_holidays
    logger.info("Actualizando SLA usando fecha de confirmación de Tareas y Feriados Chile...")
    try:
        holidays_list = get_holidays()
        query = """
            WITH task_dates AS (
                SELECT
                    ltrim(CAST(entrega AS TEXT), '0') as entrega_clean,
                    MAX(fecha_conf) as max_fecha_conf
                FROM warehouse_tasks
                WHERE fecha_conf IS NOT NULL AND fecha_conf != ''
                GROUP BY entrega_clean
            )
            SELECT
                v.rowid,
                v.creado_el,
                COALESCE(l.max_fecha_conf, v.fecha_sm_real, strftime('%d-%m-%Y','now')) as end_date
            FROM outbound_deliveries v
            LEFT JOIN task_dates l ON ltrim(CAST(v.entrega AS TEXT), '0') = l.entrega_clean
        """
        df = pd.read_sql(query, conn)

        s_date = pd.to_datetime(df['creado_el'], format='%d-%m-%Y', errors='coerce')
        e_date = pd.to_datetime(df['end_date'], format='%d-%m-%Y', errors='coerce')

        valid = s_date.notna() & e_date.notna()
        df['dias_retraso'] = np.nan

        if valid.any():
            s_values = s_date[valid].values.astype('datetime64[D]')
            e_values = e_date[valid].values.astype('datetime64[D]')

            s_bus = np.busday_offset(s_values, 0, roll='forward', holidays=holidays_list)
            e_bus = np.busday_offset(e_values, 0, roll='forward', holidays=holidays_list)

            df.loc[valid, 'dias_retraso'] = np.maximum(0, np.busday_count(s_bus, e_bus, holidays=holidays_list))

        update_data = []
        for _index, row in df[valid].iterrows():
            update_data.append((float(row['dias_retraso']), int(row['rowid'])))

        with conn:
            cursor = conn.cursor()
            # 1. Actualizar Días de Retraso (SLA)
            cursor.executemany("UPDATE outbound_deliveries SET dias_retraso = ? WHERE rowid = ?", update_data)

            # 2. Sincronizar Estado WMS: Si tiene fecha de confirmación en tareas, ya no es "OT Abierta"
            cursor.execute("""
                UPDATE outbound_deliveries
                SET estado_wms = 'Contabilizado'
                WHERE estado_wms = 'OT Abierta'
                AND EXISTS (
                    SELECT 1 FROM warehouse_tasks t
                    WHERE ltrim(CAST(t.entrega AS TEXT), '0') = ltrim(CAST(outbound_deliveries.entrega AS TEXT), '0')
                    AND t.fecha_conf IS NOT NULL
                    AND t.fecha_conf != ''
                )
            """)


        logger.info(f"SLA y Estados sincronizados con Tareas para {len(update_data)} registros. Caché invalidada.")
    except Exception as e:
        logger.error(f"Fallo en update_sla_with_tasks: {e}")

def enrich_movements_with_iw39(conn: sqlite3.Connection):
    """
    Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39_orders.
    Agrega las columnas a la tabla dinámicamente si no existen.
    Optimizada con tabla temporal indexada para procesamiento en O(N log M).
    """
    logger.info("Enriqueciendo Movimientos con Órdenes PM (IW39)...")
    try:
        # Extraer a Pandas para deduplicar y normalizar rápido
        iw39_df = pd.read_sql("SELECT orden, ceco_resp, autor FROM iw39_orders", conn)
        if iw39_df.empty:
            logger.warning("No hay ordenes IW39 para cruzar.")
            return

        iw39_df['orden_match'] = iw39_df['orden'].astype(str).str.strip().str.lstrip('0')
        iw39_df = iw39_df.drop_duplicates(subset=['orden_match'])

        with conn:
            cursor = conn.cursor()

            # Asegurar que existan las columnas en inventory_movements
            for col in ['ceco_resp', 'autor']:
                try:
                    cursor.execute(f"ALTER TABLE inventory_movements ADD COLUMN {col} TEXT")
                except sqlite3.OperationalError:
                    pass # La columna ya existe

            # Subir tabla temporal limpia e indexada
            iw39_df[['orden_match', 'ceco_resp', 'autor']].to_sql("tmp_iw39_map", conn, if_exists='replace', index=False)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tmp_iw39_orden ON tmp_iw39_map(orden_match)")

            # Realizar el cruce indexado
            cursor.execute("""
                UPDATE inventory_movements
                SET
                    ceco_resp = (SELECT ceco_resp FROM tmp_iw39_map WHERE orden_match = ltrim(CAST(inventory_movements.orden AS TEXT), '0')),
                    autor = (SELECT autor FROM tmp_iw39_map WHERE orden_match = ltrim(CAST(inventory_movements.orden AS TEXT), '0'))
                WHERE orden IS NOT NULL AND orden != ''
                AND EXISTS (
                    SELECT 1 FROM tmp_iw39_map WHERE orden_match = ltrim(CAST(inventory_movements.orden AS TEXT), '0')
                )
            """)

            cursor.execute("DROP TABLE IF EXISTS tmp_iw39_map")

        logger.info("Enriquecimiento IW39 completado.")
    except Exception as e:
        logger.error(f"Fallo en enrich_movements_with_iw39: {e}")
