## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la definición de repositorios en el sistema de monitoreo de almacén (WMS). Define funciones que proporcionan instancias de diferentes tipos de repositorios, cada uno asociado con una tabla específica en la base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Obtiene una sesión de base de datos utilizando el motor SQLAlchemy.
- `get_deliveries_repo(session: Session = Depends(get_db)) -> DeliveriesRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con las entregas.
- `get_inventory_repo(session: Session = Depends(get_db)) -> InventoryRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con el inventario.
- `get_tasks_repo(session: Session = Depends(get_db)) -> TasksRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con las tareas.
- `get_productivity_repo(session: Session = Depends(get_db)) -> ProductivityRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con la productividad.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - **DeliveriesRepository**: No especificado en el fragmento.
  - **InventoryRepository**: No especificado en el fragmento.
  - **TasksRepository**: No especificado en el fragmento.
  - **ProductivityRepository**: No especificado en el fragmento.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas: `sqlite3`, `fastapi`
- Archivos del proyecto que IMPORTA a este archivo:
  - `core.database.get_session` (importada dentro de `get_db`)
- Archivos del proyecto que este archivo IMPORTA:
  - `repositories.base.BaseRepository`
  - `repositories.deliveries.DeliveriesRepository`
  - `repositories.inventory.InventoryRepository`
  - `repositories.productivity.ProductivityRepository`
  - `repositories.tasks.TasksRepository`

Flujo de datos: Este archivo proporciona instancias de repositorios que consumen una sesión de base de datos, lo que permite a los servicios y rutas acceder a la lógica de acceso a datos.

