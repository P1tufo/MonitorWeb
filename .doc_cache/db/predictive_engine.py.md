## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa datos de movimientos en una base de datos SQLite para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Frecuencia vs Volumen y el MTBV (Media Tasa de Venta Bruta) junto con un semáforo de desplanificación.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa los movimientos de inventario para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha)
  - `ce_coste` (Centro de Costo)
  - `material` (Material)
  - `texto_breve_material` (Texto breve del material)
  - `cantidad` (Cantidad)
  - `cmv` (Código Movimiento)

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- **Librerías Externas:** 
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Flujo Interno:**
  - El archivo se ejecuta como un script principal para probar la función `generate_predictions` con una base de datos SQLite local.

