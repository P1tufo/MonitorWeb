## Archivo: ./services/background_tasks.py

### Resumen Funcional
El archivo `background_tasks.py` contiene una tarea de fondo que se encarga de refrescar las analíticas del sistema. Esta tarea ejecuta métodos de los servicios de entregas y inventario para recalcular su contexto completo.

### Catálogo de Funciones y Clases
- `refresh_analytics()` - Refresca las analíticas (ejecutado como tarea de fondo trazable).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas modificadas:
  - Ninguna (se supone que los métodos llamados internamente interactúan directamente con la base de datos).
- Consultas SQL crudas o llamadas a ORM: Sí, se usan métodos de `DeliveriesService` y `InventoryService`, que probablemente contienen consultas SQL o llamadas a ORM.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `logging`
- Archivos del proyecto que importan a este archivo (`background_tasks.py`):
  - Ninguno
- Archivos del proyecto que este archivo importa (`background_tasks.py`):
  - `core.database.get_session`
  - `routes.tasks.get_tasks_context`
  - `services.deliveries_service.DeliveriesService`
  - `services.inventory_service.InventoryService`

**Flujo de datos:**
1. `refresh_analytics()` se ejecuta.
2. Se obtiene una sesión de base de datos usando `get_session()`.
3. Se crea una instancia de `DeliveriesService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto de las entregas.
4. Se crea una instancia de `InventoryService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto del inventario.
5. Se llama a `get_tasks_context(session)`, que también probablemente realiza consultas a la base de datos.
6. Si ocurre un error, se registra con nivel de error en el logger.

Este flujo asegura que todas las operaciones relacionadas con el refresco de analíticas interactúen directamente con la base de datos a través de los servicios correspondientes.

