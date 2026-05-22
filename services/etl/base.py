from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
import sqlite3
from typing import Optional, Tuple, List
import logging

from core.security import validate_table

logger = logging.getLogger("etl-base")

class BaseWMSProcessor(ABC):
    """
    Clase abstracta unificada para procesar archivos WMS (TXT/CSV/XLSX).
    Implementa lectura optimizada por chunks y UPSERT atómico en SQLite.
    """

    def __init__(self, encodings: Optional[List[str]] = None, chunk_size: int = 50000):
        self.encodings = encodings or ['latin-1', 'cp1252', 'utf-8']
        self.chunk_size = chunk_size

    @abstractmethod
    def validate_file(self, file_path: Path) -> bool:
        """Verifica si el archivo es válido para este procesador."""
        pass

    @abstractmethod
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y transforma un chunk de datos crudos (Implementado por cada hijo)."""
        pass

    def _detect_file_params(self, file_path: Path, required_columns: List[str]) -> Tuple[int, str]:
        """Detecta la fila de encabezado y codificación buscando columnas clave."""
        for enc in self.encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    for i, line in enumerate(f):
                        if i > 100: break
                        if all(col in line for col in required_columns):
                            return i, enc
            except (UnicodeDecodeError, LookupError):
                continue
        return 0, 'latin-1'

    def read_and_clean_data(self, file_path: Path) -> pd.DataFrame:
        """Lee el archivo completo (para testing o archivos pequeños)."""
        skip, encoding = self._detect_file_params(file_path, self._get_required_columns())
        ext = file_path.suffix.lower()
        
        if ext in ['.xlsx', '.xls']:
            df_raw = pd.read_excel(file_path, skiprows=skip)
        else:
            df_raw = pd.read_csv(file_path, sep='\t', skiprows=skip, encoding=encoding, dtype=str)
            
        return self._clean_dataframe(df_raw)

    def _get_required_columns(self) -> List[str]:
        """Lista de strings que deben estar en el header para detectar el inicio. Por defecto vacía."""
        return []

    def _get_primary_keys(self) -> List[str]:
        """Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto vacía."""
        return []

    def process_and_save(self, file_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int:
        """Orquestador unificado de procesamiento Chunked + Upsert SQLite."""
        validate_table(table_name)
        path_obj = Path(file_path)
        
        if not self.validate_file(path_obj):
            logger.warning(f"Archivo no válido o no encontrado: {file_path}")
            return 0
            
        skip, encoding = self._detect_file_params(path_obj, self._get_required_columns())
        ext = path_obj.suffix.lower()
        total_processed = 0

        try:
            ctx_conn = conn if conn else sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
            if conn is None:
                ctx_conn.execute("PRAGMA journal_mode=WAL")

            with ctx_conn: # Transacción
                if ext in ['.xlsx', '.xls']:
                    # Pandas no soporta chunksize en read_excel fácilmente
                    df_raw = pd.read_excel(path_obj, skiprows=skip)
                    df_clean = self._clean_dataframe(df_raw)
                    if not df_clean.empty:
                        self._upsert_chunk(ctx_conn, df_clean, table_name)
                        total_processed += len(df_clean)
                else:
                    reader = pd.read_csv(
                        path_obj, sep='\t', skiprows=skip, 
                        encoding=encoding, dtype=str, chunksize=self.chunk_size
                    )
                    for chunk in reader:
                        df_clean = self._clean_dataframe(chunk)
                        if not df_clean.empty:
                            self._upsert_chunk(ctx_conn, df_clean, table_name)
                            total_processed += len(df_clean)
                            
                # Deduplicación final si hay primary keys
                pks = self._get_primary_keys()
                if pks:
                    group_cols = ", ".join(pks)
                    ctx_conn.execute(f"""
                        DELETE FROM {table_name}
                        WHERE rowid NOT IN (
                            SELECT MIN(rowid) FROM {table_name}
                            GROUP BY {group_cols}
                        )
                    """)
                    
            if conn is None:
                ctx_conn.close()

            logger.info(f"Procesado exitosamente: {total_processed} registros integrados en {table_name}.")
            return total_processed
            
        except Exception as e:
            logger.error(f"Fallo crítico procesando {file_path}: {e}")
            return 0

    def _upsert_chunk(self, conn: sqlite3.Connection, df: pd.DataFrame, table_name: str):
        """
        Lógica de Upsert atómico por chunk.

        ── Seguridad de los f-strings ────────────────────────────────────────
        Este método usa f-strings para interpolar nombres de tabla y columna
        en SQL. Esto es seguro porque:
          1. `table_name` se re-valida al inicio contra WHITELIST_TABLES
             (defensa en profundidad; también validado en process_and_save).
          2. `tmp_table` es derivado del `table_name` ya validado.
          3. `cols_str` y `valid_cols` provienen exclusivamente de
             `PRAGMA table_info(table_name)` — nombres reales de la BD,
             nunca de input del usuario.
        ──────────────────────────────────────────────────────────────────────
        """
        # Defensa en profundidad: re-validar table_name aunque process_and_save
        # ya lo haga. _upsert_chunk es un método público y puede llamarse directamente.
        validate_table(table_name)

        # tmp_table deriva del table_name validado — seguro para interpolación.
        tmp_table = f"tmp_{table_name}_load"
        df.to_sql(tmp_table, conn, if_exists='replace', index=False)

        cursor = conn.cursor()
        # cols_str proviene de PRAGMA table_info — nombres reales de la BD, no user input.
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]

        if not columns:
            df.to_sql(table_name, conn, if_exists='append', index=False)
        else:
            valid_cols = [c for c in df.columns if c in columns]
            cols_str = ", ".join(valid_cols)
            # table_name: validado por whitelist. cols_str: derivado de PRAGMA. tmp_table: derivado de table_name validado.
            conn.execute(f"""
                INSERT OR REPLACE INTO {table_name} ({cols_str})
                SELECT {cols_str} FROM {tmp_table}
            """)

        # tmp_table: derivado de table_name validado por whitelist.
        conn.execute(f"DROP TABLE IF EXISTS {tmp_table}")


    def process_directory(self, folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int:
        """Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo."""
        folder = Path(folder_path)
        if not folder.exists():
            logger.warning(f"Carpeta no encontrada: {folder}")
            return 0
            
        files = sorted(
            [f for f in folder.iterdir() if f.suffix.lower() in {'.txt', '.csv', '.xlsx', '.xls'} and not f.name.startswith('~')],
            key=lambda f: f.stat().st_mtime
        )
        
        if not files: return 0
        
        total_rows = 0
        for f in files:
            if self.validate_file(f):
                logger.info(f"Procesando archivo en lote: {f.name}")
                rows = self.process_and_save(str(f), db_path, table_name, conn)
                total_rows += rows
                
        return total_rows
