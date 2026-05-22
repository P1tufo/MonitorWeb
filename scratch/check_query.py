import sqlite3
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)

query_user = """
        SELECT usuario as user, 
               SUM(CASE WHEN TRIM(cmv) IN ('201', '261') 
                   AND NOT (
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%ANUL%'
                   ) THEN 1 ELSE 0 END) as qty,
               SUM(CASE WHEN TRIM(cmv) IN ('202', '262', '102', '302', '304') 
                   AND NOT (
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                       UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                       UPPER(COALESCE(referencia, '')) LIKE '%ANUL%'
                   ) THEN 1 ELSE 0 END) as anulaciones
        FROM mb51_transactions
        WHERE TRIM(cmv) IN ('201', '261', '202', '262', '102', '302', '304') AND usuario IS NOT NULL
        GROUP BY usuario
        ORDER BY qty DESC
        LIMIT 15
"""

df = pd.read_sql(query_user, conn)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df)
