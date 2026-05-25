import sqlite3

sql_abc = """
WITH MaterialCounts AS (
    SELECT 
        material as cod_mat,
        COUNT(material) as qty
    FROM inventory_movements
    WHERE cmv IN ('201', '221', '261') 
      AND material IS NOT NULL 
      AND material != ''
    GROUP BY cod_mat
),
TotalQty AS (
    SELECT SUM(qty) as total FROM MaterialCounts
),
CumSum AS (
    SELECT 
        cod_mat,
        qty,
        SUM(qty) OVER (ORDER BY qty DESC, cod_mat ASC) as cum_qty
    FROM MaterialCounts
),
Classified AS (
    SELECT 
        cod_mat,
        qty,
        CASE 
            WHEN cum_qty <= (SELECT total FROM TotalQty) * 0.80 THEN 'A (80% Frecuentes)'
            WHEN cum_qty <= (SELECT total FROM TotalQty) * 0.95 THEN 'B (15% Moderados)'
            ELSE 'C (5% Esporádicos)'
        END as categoria
    FROM CumSum
)
SELECT categoria, COUNT(cod_mat) as cantidad_items
FROM Classified
GROUP BY categoria
ORDER BY categoria ASC;
"""

conn = sqlite3.connect('data/wms_transactions.db')
cursor = conn.cursor()
cursor.execute("UPDATE config_queries SET sql_text = ? WHERE query_id = 'inv_consumos_abc'", (sql_abc,))
conn.commit()
print('ABC query updated successfully')
