import sqlite3
from db.db_enrichment import backfill_material_texts
from config import DB_PATH

def manual_fix():
    print(f"Conectando a {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    try:
        # Contar antes
        count_before = conn.execute("SELECT count(*) FROM vl06o_transactions WHERE texto_breve_de_material IS NULL OR texto_breve_de_material = ''").fetchone()[0]
        print(f"Registros sin descripción antes: {count_before}")
        
        backfill_material_texts(conn)
        
        # Contar después
        count_after = conn.execute("SELECT count(*) FROM vl06o_transactions WHERE texto_breve_de_material IS NULL OR texto_breve_de_material = ''").fetchone()[0]
        print(f"Registros sin descripción después: {count_after}")
        print(f"Éxito: Se recuperaron {count_before - count_after} descripciones.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    manual_fix()
