import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import sqlite3

from .base import BaseWMSProcessor
from core.wms_utils import (
    sanitize_string,
    map_wms_status,
    apply_cost_center_mapping,
    normalize_date_columns,
    calculate_sla_delays,
    generate_time_labels
)

class OutboundDeliveryAdapter(BaseWMSProcessor):
    """Adaptador para procesar Entregas de Salida (Deliveries)."""

    def validate_file(self, file_path: Path) -> bool:
        return file_path.exists() and file_path.suffix.lower() in ['.xlsx', '.xls', '.txt']

    def _get_required_columns(self) -> List[str]:
        # Para excel_processor solía escanear densidad de datos (count >= 15).
        # Vamos a requerir al menos 'Entrega' o 'Material' si es texto.
        return ['Entrega']

    def _get_primary_keys(self) -> List[str]:
        return ['entrega', 'pos_']

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        df.columns = self._sanitizar_nombres_columnas(df.columns)
        
        df = map_wms_status(df)
        df = apply_cost_center_mapping(df)
        df = normalize_date_columns(df)
        df = calculate_sla_delays(df)
        df = generate_time_labels(df)
        return df

    def _sanitizar_nombres_columnas(self, columns: pd.Index) -> list:
        counts: Dict[str, int] = {}
        new_cols = []
        for col in columns:
            name = sanitize_string(str(col))
            if name in counts:
                counts[name] += 1
                name = f"{name}_{counts[name]}"
            else:
                counts[name] = 0
            new_cols.append(name)
        return new_cols

    # Para Deliveries, el UPSERT original era distinto (borrado atómico por entrega y pos_).
    # Como BaseWMSProcessor ya implementa Deduplicación por Primary Keys, es suficiente.
    # Pero el DB_UPSERT original permitía agregar columnas dinámicas al esquema en SQLite.
    def _upsert_chunk(self, conn: sqlite3.Connection, df: pd.DataFrame, table_name: str):
        """Sobreescribimos para añadir sincronización de esquema como en db_upsert.py."""
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_cols = {row[1] for row in cursor.fetchall()}
        
        for col in df.columns:
            if col not in existing_cols:
                try:
                    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN "{col}"')
                    existing_cols.add(col)
                except sqlite3.Error:
                    pass
        
        # Insertar atómico usando Pandas (no replace de fila completa, solo append y luego deduplicar)
        df.to_sql(table_name, conn, if_exists='append', index=False)
