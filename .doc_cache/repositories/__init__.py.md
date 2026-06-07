## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias relacionadas con las operaciones de base de datos en un sistema de monitoreo de almacén (WMS). Define funciones para obtener conexiones a la base de datos SQLite y repositorios específicos para diferentes entidades del sistema.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de entregas utilizando la conexión proporcionada.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de inventario utilizando la conexión proporcionada.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de tareas utilizando la conexión proporcionada.
- `get_productivity_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de productividad utilizando la conexión proporcionada.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente en este archivo. Se asume que los repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`, `ProductivityRepository`) interactúan con tablas correspondientes, pero no se detalla qué columnas son utilizadas.
- **Consultas SQL Crudas o ORM:** No hay consultas SQL crudas ni llamadas a ORM directamente en este archivo. Las operaciones de base de datos se realizan a través de los métodos de los repositorios.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume):** No se especifican archivos externos que importen este archivo.
- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):** Los repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`, `ProductivityRepository`) y la configuración de base de datos (`config.py`).
- **Dirección del Flujo de Datos:** El flujo de datos comienza en las rutas (Routes), pasa por los servicios (Services) hasta llegar a este archivo para obtener una conexión a la base de datos y luego a los repositorios específicos.

