import pandas as pd
from pathlib import Path
from typing import List

from .base import BaseWMSProcessor

class WarehouseTaskAdapter(BaseWMSProcessor):
    """Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte)."""

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists(): return False
        skip, _ = self._detect_file_params(file_path, self._get_required_columns())
        return skip >= 0

    def _get_required_columns(self) -> List[str]:
        return ['OT', 'Material']

    def _get_primary_keys(self) -> List[str]:
        return ['numero_ot', 'pos']

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(axis=1, how='all')
        df.columns = [str(c).strip() for c in df.columns]
        
        mapping = {
            "N˙mero OT": "numero_ot", "Nmero OT": "numero_ot", "Pos.": "pos",
            "Material": "material", "Texto breve de material": "texto_breve_material",
            "Tp.": "tp_proc", "Ubic.proc.": "ubic_proc", "CtdTeÛrDsd": "ctd_teor_dsd",
            "CtdTerDsd": "ctd_teor_dsd", "UMA": "uma", "UbicDest": "ubic_dest",
            "Fe.creac.": "fe_creac", "Hora": "hora", "Usuario": "usuario",
            "Lote": "lote", "Cl.mov.": "cl_mov", "Clase mov.": "clase_mov",
            "Doc.mat.": "doc_mat", "Fecha conf": "fecha_conf", "HorConf": "hor_conf",
            "Ce.": "ce", "Entrega": "entrega"
        }

        df_cols = list(df.columns)
        new_cols = []
        tp_count = 0
        usuario_count = 0
        
        for col in df_cols:
            c = str(col).strip()
            base_name = c.split('.')[0] if '.' in c and c.split('.')[-1].isdigit() else c
            base_name = base_name.rstrip('.')
            
            if base_name == "Tp":
                new_cols.append("tp_proc" if tp_count == 0 else "tp_dest")
                tp_count += 1
            elif base_name == "Usuario":
                new_cols.append("usuario" if usuario_count == 0 else "usuario_conf")
                usuario_count += 1
            elif c in mapping: new_cols.append(mapping[c])
            elif base_name in mapping: new_cols.append(mapping[base_name])
            else:
                if "OT" in c: new_cols.append("numero_ot")
                elif "Pos" in c: new_cols.append("pos")
                elif "Ctd" in c: new_cols.append("ctd_teor_dsd")
                else: new_cols.append(c.lower().replace('.', '').replace(' ', '_'))
        
        df.columns = new_cols
        
        df = df.dropna(subset=['material'])
        df = df[df['material'].astype(str).str.strip() != '']
        
        for col in ['fe_creac', 'fecha_conf']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('.', '-', regex=False)

        if 'ctd_teor_dsd' in df.columns:
            df['ctd_teor_dsd'] = df['ctd_teor_dsd'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            df['ctd_teor_dsd'] = pd.to_numeric(df['ctd_teor_dsd'], errors='coerce').fillna(0).abs()
        
        df['material'] = df['material'].astype(str).str.strip().str.lstrip('0')
        if 'numero_ot' in df.columns:
            df['numero_ot'] = df['numero_ot'].astype(str).str.strip().str.lstrip('0')
        if 'pos' in df.columns:
            df['pos'] = df['pos'].astype(str).str.strip().str.lstrip('0')
        
        return df.drop_duplicates(subset=self._get_primary_keys()).reset_index(drop=True)
