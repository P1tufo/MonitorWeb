import sqlite3
from routes.tasks import get_tasks_context

def diag_dashboard():
    conn = sqlite3.connect('/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db')
    print("Generating context...")
    context = get_tasks_context(conn)
    
    print("--- NON PALLETIZED SUMMARY (Top 5) ---")
    summary = context.get('non_palletized_summary', [])
    for row in summary[:5]:
        print(row)
        
    print("\n--- NON PALLETIZED MOVEMENTS (Top 5) ---")
    movs = context.get('non_palletized_movements', [])
    for row in movs[:5]:
        print(row)
        
    conn.close()

if __name__ == '__main__':
    diag_dashboard()
