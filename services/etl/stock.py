import pandas as pd
from pathlib import Path
from typing import List, Optional
import sqlite3
import os
from datetime import datetime
import logging

from .base import BaseWMSProcessor

logger = logging.getLogger("etl-stock")

class StockLevelAdapter(BaseWMSProcessor):
    """Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo."""

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists(): return False
        skip, _ = self._detect_file_params(file_path, self._get_required_columns())
        return skip >= 0

    def _get_required_columns(self) -> List[str]:
        # Suponemos que requiere OT(cuanto) o Material
        return []

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return df
        
        # Eliminamos filas y columnas totalmente vacías
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        # Limpieza de strings
        str_cols = df.select_dtypes(include=['object']).columns
        for c in str_cols:
            df[c] = df[c].astype(str).str.strip()
            
        return df

    def process_directory(self, folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int:
        """Sobreescribe process_directory para combinar todos los archivos y hacer REPLACE."""
        folder = Path(folder_path)
        if not folder.exists():
            logger.warning(f"Carpeta {folder_path} no existe.")
            return 0

        files = [f for f in folder.iterdir() if f.suffix.lower() in {'.txt', '.csv', '.xlsx', '.xls'} and not f.name.startswith('~')]
        if not files: return 0

        all_dfs = []
        for file_path in files:
            try:
                # Usamos read_and_clean_data
                df = self.read_and_clean_data(file_path)
                if not df.empty and 'otcuanto' in df.columns:
                    df['source_file'] = file_path.name
                    df['ingested_at'] = datetime.now().isoformat()
                    all_dfs.append(df)
            except Exception as e:
                logger.error(f"Fallo al procesar {file_path.name}: {e}")

        if not all_dfs: return 0

        combined_df = pd.concat(all_dfs, ignore_index=True)
        rows = len(combined_df)
        
        ctx_conn = conn if conn else sqlite3.connect(db_path)
        try:
            combined_df.to_sql(table_name, ctx_conn, if_exists="replace", index=False)
            ctx_conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_otcuanto ON {table_name}(otcuanto)")
        except Exception as e:
            logger.error(f"Fallo guardando stock en DB: {e}")
            rows = 0
        finally:
            if conn is None:
                ctx_conn.close()
                
        return rows
