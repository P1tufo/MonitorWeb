import pandas as pd
import numpy as np
from pathlib import Path
from typing import List

from .base import BaseWMSProcessor

class InventoryMovementAdapter(BaseWMSProcessor):
    """Adaptador específico para procesar el formato WMS Movimientos."""

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists(): return False
        skip, _ = self._detect_file_params(file_path, self._get_required_columns())
        return skip >= 0

    def _get_required_columns(self) -> List[str]:
        return ['Fe.contab.', 'Material']

    def _get_primary_keys(self) -> List[str]:
        return ['doc_mat', 'ej_mat', 'pos']

    def _clean_dataframe(self, chunk: pd.DataFrame) -> pd.DataFrame:
        chunk = chunk.dropna(axis=1, how='all')
        chunk.columns = [str(c).strip() for c in chunk.columns]
        
        mapping = {
            "Fe.contab.": "fe_contab", "Alm.": "alm", "Ce.": "ce",
            "CMv": "cmv", "Referencia": "referencia", "Texto cab.documento": "texto_cab_documento",
            "Texto breve de material": "texto_breve_material", "Material": "material",
            "Cantidad": "cantidad", "UMB": "umb", "Doc.mat.": "doc_mat",
            "EjMat": "ej_mat", "Registrado": "registrado", "Hora": "hora",
            "Usuario": "usuario", "Pedido": "pedido", "Ce.coste": "ce_coste",
            "Importe ML": "importe_ml", "Mon.": "mon", "Proveedor": "proveedor"
        }
        
        new_cols = []
        for col in chunk.columns:
            clean_col = col.strip()
            if clean_col == "Pos": new_cols.append("pos")
            elif clean_col == "Pos.": new_cols.append("pos_extra")
            elif clean_col in mapping: new_cols.append(mapping[clean_col])
            else: new_cols.append(clean_col.lower().replace('.', '').replace(' ', '_'))
        chunk.columns = new_cols
        
        db_columns = list(mapping.values()) + ['pos', 'pos_extra', 'tipo_operacion']
        valid_cols = [c for c in chunk.columns if c in db_columns]
        chunk = chunk[valid_cols]
        chunk = chunk.loc[:, ~chunk.columns.duplicated()]
        
        if 'doc_mat' in chunk.columns:
            chunk = chunk.dropna(subset=['doc_mat'])
            chunk = chunk[chunk['doc_mat'].str.strip() != '']
            chunk = chunk[~chunk['doc_mat'].str.contains(r'^-+$', na=False)]
            
        if 'fe_contab' in chunk.columns:
            chunk['fe_contab'] = chunk['fe_contab'].astype(str).str.replace('.', '-', regex=False)
            
        if 'cantidad' in chunk.columns:
            clean_qty = chunk['cantidad'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.rstrip('-')
            chunk['cantidad'] = pd.to_numeric(clean_qty, errors='coerce').fillna(0)
            
        if 'importe_ml' in chunk.columns:
            clean_imp = chunk['importe_ml'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.rstrip('-')
            chunk['importe_ml'] = pd.to_numeric(clean_imp, errors='coerce').fillna(0)
            
        return self._vectorized_classify(chunk)

    def _vectorized_classify(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'cmv' not in df.columns: return df
        cmv = df['cmv'].astype(str)
        cant = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0)
        conditions = [
            (cmv == '101'), (cmv == '261'), (cmv == '201'), (cmv == '303'),
            (cmv == '301') & (cant > 0), (cmv == '301') & (cant <= 0), (cmv.isin(['262', '202']))
        ]
        choices = [
            'Ingreso', 'Consumo (Orden/Reserva)', 'Consumo (Centro Costo)',
            'Traspaso (Salida)', 'Traspaso (Ingreso)', 'Traspaso (Salida)', 'Devolucion'
        ]
        df['tipo_operacion'] = np.select(conditions, choices, default='Otro')
        return df
