import sqlite3

def test_query():
    conn = sqlite3.connect('/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db')
    cursor = conn.cursor()
    
    query = """
        SELECT 
            p.otcuanto as doc_mat,
            m.pos,
            p.material,
            p.denominacion as material_name,
            p.stock_disp as qty,
            m.alm as source,
            m.ce as dest,
            m.fe_contab || ' ' || m.hora as created_at
        FROM lx02_pendientes p
        JOIN inventory_movements m ON p.otcuanto = m.doc_mat
        WHERE m.usuario = ? AND m.cmv = ?
          AND CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
        LIMIT 10
    """
    
    user = 'CVALDERRAMA'
    clase_mov = '101'
    # Try string and int
    print("Testing with strings:", user, clase_mov)
    cursor.execute(query, (user, clase_mov))
    rows = cursor.fetchall()
    print("Results:", len(rows))
    
    print("Testing with int:", user, int(clase_mov))
    cursor.execute(query, (user, int(clase_mov)))
    rows = cursor.fetchall()
    print("Results:", len(rows))
    
    conn.close()

if __name__ == '__main__':
    test_query()
