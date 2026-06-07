## Archivo: ./scripts/run_consolidator.py

### Resumen Funcional
El archivo `run_consolidator.py` es un script que ejecuta la consolidación de transacciones del almacén. Recibe como parámetro el camino a una carpeta y utiliza la clase `DataConsolidator` para procesar y consolidar los datos de las transacciones almacenados en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `main()` - Función principal que verifica si se proporciona un argumento (camino a la carpeta) y luego llama al método `consolidate_folder` de la clase `DataConsolidator`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. La base de datos se especifica en el parámetro del constructor de `DataConsolidator`.
- Consultas SQL Crudas o ORM: Ninguna.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías Externas:
  - `pathlib`: Para manejar rutas de archivos.
  - `os`: Para manipular el sistema operativo.
- Archivos del Proyecto que Importan a este Archivo: Ninguno.
- Archivos del Proyecto que Este Archivo Importa:
  - `config.DB_PATH`: Ruta de la base de datos.
  - `db.consolidator.DataConsolidator`: Clase para la consolidación de datos.

**Flujo de Datos:**
1. El script se ejecuta desde la línea de comandos con un argumento que es el camino a una carpeta.
2. La función `main()` verifica si se proporciona el argumento necesario.
3. Se crea una instancia de `DataConsolidator` con la ruta a la base de datos SQLite.
4. El método `consolidate_folder` de `DataConsolidator` es llamado para procesar y consolidar los datos en la carpeta especificada.

Este flujo asegura que el script se comporte correctamente cuando se ejecuta desde la línea de comandos con el argumento adecuado.

