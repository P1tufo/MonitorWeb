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
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

**Flujo de Datos:**
1. El archivo se ejecuta directamente (`if __name__ == "__main__"`).
2. Se importan las dependencias necesarias.
3. La función `generate_predictions` se invoca con la ruta a la base de datos SQLite.
4. Los movimientos de inventario son leídos desde la tabla `inventory_movements`.
5. El procesamiento y análisis de los datos ocurren dentro de la función.
6. Los resultados (combos, scatter data y alertas) se devuelven como un diccionario.

**Dirección del Flujo:**
- **Entrada:** Ruta a la base de datos SQLite.
- **Procesamiento:** Análisis de movimientos de inventario.
- **Salida:** Resultados en formato JSON.

