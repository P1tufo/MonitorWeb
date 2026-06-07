## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la validación de fechas, la protección contra nombres de tabla no seguros y la lógica de sobrescritura de archivos más recientes.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas desde nombres de archivo sea correcto.
- `test_validate_table_security(consolidator)` - Valida la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite (indicado por la cadena de conexión `":memory:"`)
- Tablas:
  - `TABLE_DELIVERIES`
  - `TABLE_STOCK`
- Columnas: No se especifican explícitamente, pero se asume que las columnas coinciden con el esquema de las tablas en la base de datos.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pytest`
- Archivos del proyecto que importa:
  - `core.security.validate_table`
  - `db.consolidator.DataConsolidator`
  - `db.consolidator.StockLevelAdapter.read_and_clean_data`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El archivo no realiza operaciones directas sobre archivos o bases de datos, sino que interactúa con objetos inyectados y mockeados para probar la lógica de negocio.

