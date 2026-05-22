import sqlite3
import pandas as pd

DB_PATH = "data/wms_transactions.db"
conn = sqlite3.connect(DB_PATH)

print("--- Outbound Deliveries sample ---")
df = pd.read_sql("SELECT entrega, ubicacion_area, area_negocio, centro FROM outbound_deliveries LIMIT 15", conn)
print(df.to_string())

print("\n--- Config Cost Center Mapping ---")
mapping_df = pd.read_sql("SELECT * FROM config_cost_center_mapping", conn)
print(mapping_df.to_string())

print("\n--- Recent transactions with query logic ---")
query = """
    SELECT 
        v.entrega,
        v.area_negocio as raw_area_negocio,
        v.ubicacion_area as raw_ubicacion_area,
        m.business_area as mapped_area,
        SUBSTR(v.ubicacion_area, 1, 6) as sub_code,
        CASE 
            WHEN m.business_area IS NOT NULL THEN m.business_area
            WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
            WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
            ELSE 'S/N' 
        END as area_val
    FROM outbound_deliveries v
    LEFT JOIN config_cost_center_mapping m ON SUBSTR(v.ubicacion_area, 1, 6) = m.center_code
    LIMIT 20
"""
tx_df = pd.read_sql(query, conn)
print(tx_df.to_string())
conn.close()
