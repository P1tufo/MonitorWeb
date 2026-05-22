import sqlite3
import pandas as pd

import os
from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from config import DB_PATH
conn = sqlite3.connect(str(DB_PATH))

areas_df = pd.read_sql(
    "SELECT DISTINCT [area_negocio], MAX([centro]) as centro "
    "FROM vl06o_transactions WHERE [area_negocio] IS NOT NULL GROUP BY [area_negocio]",
    conn
)

manual_map = {
    'VIGAS': 'Aserradero',
    'ASERRADERO': 'Aserradero',
    'REMANUFACTURA': 'Aserradero'
}

area_centro_map = {}
for _, row in areas_df.iterrows():
    a = str(row['area_negocio'])
    c = row['centro']
    if pd.isna(c) or str(c).strip() in ["", "nan", "None"]:
        c = 'Aserradero' if a in ['VIGAS', 'ASERRADERO', 'REMANUFACTURA'] else 'Paneles'
    area_centro_map[a] = c

print(area_centro_map)
conn.close()
