## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias de los repositorios en una aplicación FastAPI que utiliza SQLite como base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con entregas.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con el inventario.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con tareas.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas y Columnas: No aplica (se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`)
- Consultas SQL Crudas o ORM: Se utiliza el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `fastapi`: Para manejar las dependencias en FastAPI.
- Comunicación con otros archivos del proyecto:
  - Importa clases y funciones desde los módulos `base.py`, `deliveries.py`, `inventory.py` y `tasks.py`.

