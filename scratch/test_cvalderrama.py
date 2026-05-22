import sqlite3

def test_query():
    conn = sqlite3.connect('/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db')
    cursor = conn.cursor()
    
    query = """
        SELECT 
            m.usuario,
            m.cmv,
            COUNT(*)
        FROM lx02_pendientes p
        JOIN inventory_movements m ON p.otcuanto = m.doc_mat
        WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
        GROUP BY m.usuario, m.cmv
    """
    
    cursor.execute(query)
    found = False
    for row in cursor.fetchall():
        u, c, count = row
        if u and 'CVALDERRAMA' in u:
            print(f"Found match: User='{u}', CMV='{c}' (len={len(str(c))}), Count={count}")
            found = True
            
    if not found:
        print("CVALDERRAMA not found!")

if __name__ == '__main__':
    test_query()
