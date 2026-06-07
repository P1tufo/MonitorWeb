from pathlib import Path
from typing import List

import pandas as pd

from .base import BaseWMSProcessor


class MB5BProcessor(BaseWMSProcessor):
    """Adaptador específico para procesar el formato MB5B (Stock Inicial)."""

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            return False
        skip, _ = self._detect_file_params(file_path, self._get_required_columns())
        return skip >= 0

    def _get_required_columns(self) -> List[str]:
        # Identificadores clave del reporte MB5B
        return ['Material', 'Stock inicial']

    def _get_primary_keys(self) -> List[str]:
        # Para MB5B asumimos que hay una fila por material
        return ['material']

    def _clean_dataframe(self, chunk: pd.DataFrame) -> pd.DataFrame:
        # Eliminar columnas vacías
        chunk = chunk.dropna(axis=1, how='all')
        chunk.columns = [str(c).strip() for c in chunk.columns]

        # Mapeo flexible debido a posibles problemas de encoding en la cabecera
        new_cols = []
        for col in chunk.columns:
            clean_col = col.strip()
            if clean_col == "Material":
                new_cols.append("material")
            elif "Stock inicial" in clean_col:
                new_cols.append("stock_inicial")
            elif clean_col == "UMB":
                new_cols.append("umb")
            else:
                new_cols.append(clean_col.lower().replace('.', '').replace(' ', '_'))
        chunk.columns = new_cols

        # Filtrar columnas requeridas
        required = ["material", "stock_inicial", "umb"]
        valid_cols = [c for c in required if c in chunk.columns]
        chunk = chunk[valid_cols]
        chunk = chunk.loc[:, ~chunk.columns.duplicated()]

        # Limpieza de material
        if 'material' in chunk.columns:
            chunk = chunk.dropna(subset=['material'])
            chunk = chunk[chunk['material'].astype(str).str.strip() != '']
            chunk['material'] = chunk['material'].astype(str).str.strip().str.lstrip('0')

        # Limpieza de stock numérico (ej. "78,000", "2.000,000")
        if 'stock_inicial' in chunk.columns:
            # Eliminar puntos de miles y reemplazar coma por punto
            chunk['stock_inicial'] = (
                chunk['stock_inicial']
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            # Convertir a float
            chunk['stock_inicial'] = pd.to_numeric(chunk['stock_inicial'], errors='coerce').fillna(0.0)

        if 'umb' in chunk.columns:
            chunk['umb'] = chunk['umb'].astype(str).str.strip()

        return chunk
