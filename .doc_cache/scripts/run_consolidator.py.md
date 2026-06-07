## Archivo: ./scripts/run_consolidator.py

### Resumen Funcional
El archivo `run_consolidator.py` es un script que ejecuta la consolidación de datos en una carpeta especificada utilizando el motor de base de datos SQLite. El script recibe como argumento la ruta de la carpeta a procesar y utiliza una instancia de `DataConsolidator` para realizar la consolidación.

### Catálogo de Funciones y Clases
- `main()` - Función principal que verifica si se proporciona un argumento (ruta de la carpeta) y luego ejecuta el método `consolidate_folder` de la clase `DataConsolidator`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. El script no realiza consultas directas a la base de datos.

### Estado y Variables Globales
- Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- Librerías externas: `os`, `sys`
- Archivos del proyecto que importa:
  - `config.py` (para obtener la ruta de la base de datos)
  - `db.consolidator.DataConsolidator` (clase para la consolidación de datos)

- Archivos del proyecto que son importados por este archivo: Ninguno.

**Flujo de Datos:** El script recibe una ruta de carpeta como argumento, crea una instancia de `DataConsolidator`, y llama al método `consolidate_folder` con la ruta proporcionada.

