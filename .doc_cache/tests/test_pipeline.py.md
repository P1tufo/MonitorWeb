## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de análisis de fechas, validación de nombres de tablas y lógica de sobrescritura de archivos.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security(consolidator)` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
- Motor: SQLite (in-memory)
- Tablas:
  - `TABLE_DELIVERIES`
  - `TABLE_STOCK`
- Columnas: No especificadas explícitamente en el código proporcionado.
- Consultas SQL crudas o llamadas a ORM: No se observan consultas específicas.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
- Archivos del proyecto que este archivo importa (consume):
  - `db.consolidator.DataConsolidator`
  - `services.etl.OutboundDeliveryAdapter.read_and_clean_data`
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguna.
- Dirección del flujo de datos: El archivo consume funciones y clases de otros módulos para realizar pruebas unitarias.

