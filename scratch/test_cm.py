import sqlite3
import pandas as pd
from datetime import datetime
from config import DB_PATH
from core.analytics_queries import (
    get_vl06o_area_stats, get_vl06o_top_authors, get_vl06o_top_locations, get_vl06o_top_materials_by_area
)

conn = sqlite3.connect(DB_PATH)
current_year = datetime.now().year
current_month_str = f"-{datetime.now().month:02d}-{current_year}"

area_stats = get_vl06o_area_stats(conn, current_year)
area_stats_cm = get_vl06o_area_stats(conn, current_month_str)
area_stats_cm = area_stats_cm.rename(columns={'total_entregas': 'total_entregas_cm', 'dias_activos': 'dias_activos_cm'})
area_stats = pd.merge(area_stats, area_stats_cm[['area', 'total_entregas_cm', 'dias_activos_cm']], on='area', how='left').fillna(0)

print("Area Stats Columns:", area_stats.columns.tolist())
print(area_stats.head())

conn.close()
