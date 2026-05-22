## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa datos de movimientos en una base de datos SQLite para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y la Estacionalidad Diaria Semana (DOW Bias). El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la planificación y desplanificación.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa Movimientos Transactions para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab`, `ce_coste`, `material`, `texto_breve_material`, `cantidad`, `cmv`

### Estado y Variables Globales
No aplica

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

- **Flujo Interno:** El archivo se comunica con el módulo `core.wms_config` para obtener una consulta específica y realiza operaciones de análisis y procesamiento en los datos leídos desde la base de datos SQLite.

