import sqlite3

def diag():
    conn = sqlite3.connect('/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db')
    cursor = conn.cursor()
    
    query = """
        SELECT 
            m.usuario as user,
            m.cmv as clase_mov,
            COUNT(*) as count
        FROM lx02_pendientes p
        JOIN inventory_movements m ON p.otcuanto = m.doc_mat
        WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
        GROUP BY m.usuario, m.cmv
        ORDER BY count DESC
        LIMIT 5
    """
    
    cursor.execute(query)
    for row in cursor.fetchall():
        user, cmv, count = row
        print(f"User: '{user}' (len: {len(user) if user else 0}), CMV: '{cmv}' (len: {len(str(cmv))}), Count: {count}")

if __name__ == '__main__':
    diag()
