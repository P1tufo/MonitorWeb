"""
db/consolidator.py — Orquestador de consolidación de datos con persistencia segura.
"""
import os
import sqlite3
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Final

from services.etl import OutboundDeliveryAdapter
from .db_enrichment import (
    learn_author_areas, 
    apply_author_learning, 
    enrich_deliveries_with_stock as _enrich_with_stock, 
    backfill_deliveries_from_movements as _backfill_movements,
    backfill_material_texts as _backfill_texts,
    update_sla_with_tasks as _update_sla_tasks
)

# Configuración de Logging
logger = logging.getLogger("db-consolidator")

# Constantes de Base de Datos
from core.security import validate_table

TABLE_DELIVERIES: Final[str] = "outbound_deliveries"
TABLE_STOCK: Final[str] = "stock_levels"

class DataConsolidator:
    """
    Gestiona la consolidación de archivos WMS en SQLite.
    Soporta el protocolo de context manager (with statement).
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """Establece la conexión y configura optimizaciones de SQLite."""
        try:
            # Aumentar timeout para evitar bloqueos durante sincronización pesada
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30.0)
            # Optimización para concurrencia y velocidad
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            logger.debug(f"Conexión establecida con {self.db_path} (WAL Mode)")
        except sqlite3.Error as e:
            logger.error(f"Error conectando a la DB: {e}")
            raise

    def _parse_file_date(self, file_path: Path) -> datetime:
        """Extrae la fecha del nombre del archivo (dd-mm-yyyy)."""
        match = re.match(r'^(\d{2}[-\.]\d{2}[-\.]\d{4})_', file_path.name)
        if match:
            date_str = match.group(1).replace('.', '-')
            try:
                return datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                pass
        return datetime.min

    def consolidate_folder(self, folder_path: str, table_name: str = TABLE_DELIVERIES):
        """Consolida archivos cronológicamente mediante lógica UPSERT."""
        validate_table(table_name)
        folder = Path(folder_path)
        files = sorted(folder.glob("*.xlsx"), key=self._parse_file_date)

        if not files:
            logger.warning(f"No se encontraron archivos .xlsx en {folder_path}")
            return

        logger.info(f"Consolidando {len(files)} archivos en '{table_name}'...")

        total = 0
        from core.wms_utils import is_file_changed, mark_file_processed
        
        for file_path in files:
            try:
                if is_file_changed(self.conn, file_path):
                    rows = OutboundDeliveryAdapter().process_and_save(str(file_path), self.db_path, table_name, self.conn)
                    mark_file_processed(self.conn, file_path, row_count=rows)
                    total += rows
                    logger.info(f"Archivo procesado: {file_path.name} ({rows} filas)")
                else:
                    logger.debug(f"Saltando archivo (sin cambios): {file_path.name}")
            except Exception as e:
                logger.error(f"Error procesando {file_path.name}: {e}")

        # Post-procesamiento (Solo si hubo cambios)
        if total > 0:
            try:
                learn_author_areas(self.conn)
                apply_author_learning(self.conn, table_name)
                logger.info(f"Procesamiento completado. Registros afectados: {total}")
            except Exception as e:
                logger.error(f"Error en post-procesamiento de autores: {e}")
            
        return total

    def overwrite_with_latest(self, folder_path: str, table_name: str = TABLE_STOCK):
        """Reemplaza la tabla con los datos del archivo más reciente."""
        validate_table(table_name)
        folder = Path(folder_path)
        files = [f for f in folder.iterdir() if f.suffix.lower() in {'.txt', '.xlsx'} and '_' in f.name]

        if not files:
            logger.warning(f"No hay archivos válidos para sobrescribir '{table_name}'")
            return

        files.sort(key=self._parse_file_date, reverse=True)
        latest = files[0]
        logger.info(f"Actualizando '{table_name}' usando archivo más reciente: {latest.name}")

        try:
            df = OutboundDeliveryAdapter().read_and_clean_data(latest)

            if not df.empty:
                rows = len(df)
                df['source_file'] = latest.name
                df['ingested_at'] = datetime.now().isoformat()
                df.to_sql(table_name, self.conn, if_exists='replace', index=False)
                logger.info(f"Tabla '{table_name}' reemplazada con {rows} filas.")
                return rows
        except Exception as e:
            logger.error(f"Fallo al sobrescribir tabla '{table_name}': {e}")
            return 0

    def enrich_deliveries_with_stock(self):
        """Enriquece las transacciones con información de stock actual."""
        _enrich_with_stock(self.conn)

    def backfill_from_movements(self):
        """Sincroniza datos faltantes desde la tabla Movimientos."""
        _backfill_movements(self.conn)

    def backfill_texts(self):
        """Sincroniza descripciones faltantes desde Stock y Movimientos."""
        _backfill_texts(self.conn)

    def update_sla_with_tasks(self):
        """Actualiza el SLA cruzando fechas con Tareas."""
        _update_sla_tasks(self.conn)

    def close(self):
        """Cierra la conexión de forma segura."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.debug("Conexión a DB cerrada.")

# Lógica de CLI separada
def main():
    import sys
    from config import DB_PATH
    
    if len(sys.argv) < 2:
        print("Uso: python -m db.consolidator <folder_path>")
        return

    folder = sys.argv[1]
    with DataConsolidator(DB_PATH) as dc:
        dc.consolidate_folder(folder)

if __name__ == "__main__":
    main()
