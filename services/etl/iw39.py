import pandas as pd
from pathlib import Path
from typing import List

from .base import BaseWMSProcessor

class IW39Processor(BaseWMSProcessor):
    """Adaptador específico para procesar el formato IW39 (Órdenes PM)."""

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists(): return False
        skip, _ = self._detect_file_params(file_path, self._get_required_columns())
        return skip >= 0

    def _get_required_columns(self) -> List[str]:
        # Identificadores clave del reporte IW39
        return ['Orden', 'Ce.coste', 'CeCo resp.']

    def _get_primary_keys(self) -> List[str]:
        return ['orden']

    def _clean_dataframe(self, chunk: pd.DataFrame) -> pd.DataFrame:
        # Eliminar columnas vacías
        chunk = chunk.dropna(axis=1, how='all')
        chunk.columns = [str(c).strip() for c in chunk.columns]
        
        # Mapeo de columnas requeridas
        mapping = {
            "Orden": "orden",
            "Ce.coste": "ce_coste",
            "CeCo resp.": "ceco_resp",
            "Autor": "autor",
            "Elemento PEP": "elemento_pep",
            "Inic.extr.": "inic_extr"
        }
        
        new_cols = []
        for col in chunk.columns:
            clean_col = col.strip()
            if clean_col in mapping:
                new_cols.append(mapping[clean_col])
            else:
                new_cols.append(clean_col.lower().replace('.', '').replace(' ', '_'))
        chunk.columns = new_cols
        
        db_columns = list(mapping.values())
        valid_cols = [c for c in chunk.columns if c in db_columns]
        chunk = chunk[valid_cols]
        chunk = chunk.loc[:, ~chunk.columns.duplicated()]
        
        # Filtrar filas sin Orden (clave primaria)
        if 'orden' in chunk.columns:
            chunk = chunk.dropna(subset=['orden'])
            chunk = chunk[chunk['orden'].astype(str).str.strip() != '']
            chunk['orden'] = chunk['orden'].astype(str).str.strip().str.lstrip('0')
            
        # Limpieza de fechas si es necesario
        if 'inic_extr' in chunk.columns:
            chunk['inic_extr'] = chunk['inic_extr'].astype(str).str.replace('.', '-', regex=False)
            
        # Normalizar Ce.coste y CeCo resp.
        if 'ce_coste' in chunk.columns:
            chunk['ce_coste'] = chunk['ce_coste'].astype(str).str.strip().str.upper()
        if 'ceco_resp' in chunk.columns:
            chunk['ceco_resp'] = chunk['ceco_resp'].astype(str).str.strip().str.upper()
            
        return chunk
