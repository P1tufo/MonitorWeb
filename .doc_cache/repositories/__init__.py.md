## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y gestión de las dependencias relacionadas con la base de datos en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define funciones para obtener conexiones a la base de datos y repositorios específicos para diferentes entidades del sistema.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite utilizando el motor `sqlite3` y devuelve un contexto manejador que cierra la conexión cuando se sale del bloque.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db)) -> DeliveriesRepository` - Crea e inicializa una instancia del repositorio `DeliveriesRepository` con la conexión a la base de datos proporcionada.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db)) -> InventoryRepository` - Crea e inicializa una instancia del repositorio `InventoryRepository` con la conexión a la base de datos proporcionada.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db)) -> TasksRepository` - Crea e inicializa una instancia del repositorio `TasksRepository` con la conexión a la base de datos proporcionada.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente en este archivo. Se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`.
- **Consultas SQL Crudas o ORM:** Utiliza el motor `sqlite3` directamente para establecer la conexión.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume):** No se detectan archivos externos que importen este archivo.
- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):** Los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`.
- **Dirección del Flujo de Datos:** El flujo de datos comienza en las rutas FastAPI, pasa por los servicios, luego a través de estas funciones para obtener la conexión a la base de datos y los repositorios correspondientes.

