## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa los movimientos de inventario para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y el Índice MTBV con Semáforo de Desplanificación. El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la gestión del almacén.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa movimientos de inventario para generar modelos predictivos.

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
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `os`
  - `sqlite3`
  - `sys`
  - `collections.Counter`
  - `datetime`
  - `itertools.combinations`
  - `numpy`
  - `pandas`

- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

- **Flujo de Datos:**
  - El archivo importa configuraciones y dependencias necesarias.
  - Llama a la función `generate_predictions` con el camino a la base de datos.
  - La función procesa los datos, realiza análisis predictivos y devuelve resultados.

### Notas Adicionales
- La función `generate_predictions` maneja excepciones y registra errores utilizando `logging`.
- El archivo incluye un bloque de prueba al final para ejecutar la función y mostrar el número de combos, puntos de dispersión y alertas generados.

