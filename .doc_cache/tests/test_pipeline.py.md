## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos, utilizando la biblioteca `pytest`. Las pruebas cubren la funcionalidad de análisis de fechas en archivos, validación de nombres de tablas y lógica de sobrescritura de archivos más recientes.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security(consolidator)` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos).
- Tablas: No aplica (No hay consultas SQL crudas o llamadas a ORM).
- Columnas: No aplica (No se manipulan columnas específicas).

### Estado y Variables Globales
- No aplica (No se definen variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico).

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
- Comunicación con otros archivos del proyecto:
  - `db.consolidator.DataConsolidator` (fixture)
  - `services.etl.OutboundDeliveryAdapter.read_and_clean_data` (mockeado)

