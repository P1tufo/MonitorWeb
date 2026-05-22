import sqlite3
import pandas as pd
import numpy as np

# Feriados de Chile (ejemplo 2024-2026, lo mínimo necesario)
CHILEAN_HOLIDAYS = [
    '2024-01-01', '2024-03-29', '2024-03-30', '2024-05-01', '2024-05-21', 
    '2024-06-09', '2024-06-20', '2024-07-16', '2024-08-15', '2024-09-18', 
    '2024-09-19', '2024-09-20', '2024-10-12', '2024-10-27', '2024-10-31', 
    '2024-11-01', '2024-12-08', '2024-12-25',
    '2025-01-01', '2025-04-18', '2025-04-19', '2025-05-01', '2025-05-21', 
    '2025-06-20', '2025-07-16', '2025-08-15', '2025-09-18', '2025-09-19', 
    '2025-10-12', '2025-10-31', '2025-11-01', '2025-12-08', '2025-12-25',
    '2026-01-01', '2026-04-03', '2026-04-04', '2026-05-01', '2026-05-21',
    '2026-06-21', '2026-07-16', '2026-08-15', '2026-09-18', '2026-09-19',
    '2026-10-12', '2026-10-31', '2026-11-01', '2026-12-08', '2026-12-25'
]

def calculate_efficiency():
    conn = sqlite3.connect('db/data.db') # wait, path is config.DB_PATH
    import sys
    sys.path.append('.')
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    
    df = pd.read_sql("SELECT fe_contab, registrado FROM mb51_transactions WHERE fe_contab IS NOT NULL AND registrado IS NOT NULL AND length(fe_contab) >= 10 AND length(registrado) >= 10", conn)
    
    def parse_date(date_series):
        # Format can be DD.MM.YYYY or DD-MM-YYYY
        return pd.to_datetime(date_series, format='mixed', dayfirst=True, errors='coerce')
        
    df['fe_contab_dt'] = parse_date(df['fe_contab']).dt.date
    df['registrado_dt'] = parse_date(df['registrado']).dt.date
    
    df = df.dropna()
    
    if df.empty:
        return 0, 0
        
    # Calcular business days
    # busday_count accounts for weekends by default
    diffs = np.busday_count(
        list(df['fe_contab_dt']), 
        list(df['registrado_dt']), 
        holidays=CHILEAN_HOLIDAYS
    )
    
    df['diff'] = diffs
    
    # Consideramos eficiente si diff <= 0 (registrado <= fe_contab) o diff == 0 (mismo día hábil)
    # The requirement: "compararás columna registrado vs fe_contab ignorando sabados, domingos y feriados"
    # Usually, if difference is 0 or 1 working days? "eficiencia de bodega"
    # Let's say if diff == 0 it's 100% efficient (done the exact same day). 
    efficient = df['diff'] <= 0
    eff_rate = round((efficient.sum() / len(df)) * 100, 1)
    
    return eff_rate, len(df)

print(calculate_efficiency())
