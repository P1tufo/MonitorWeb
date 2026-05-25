## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas en un sistema SaaS. Este contexto incluye información sobre widgets, áreas de negocio, y otros datos relevantes.

### Catálogo de Funciones y Clases
- **DeliveriesService(session: Session)** - Inicializa el servicio con una sesión de base de datos.
- **get_full_context() -> Dict[str, Any]** - Genera un contexto completo para las entregas, incluyendo widgets, áreas de negocio, y otros datos.

### Interacción con Base de Datos
- **Motor:** SQLite (deducido del uso de `Session` de SQLAlchemy).
- **Tablas:** `outbound_deliveries`.
- **Columnas:** `area_negocio`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías Externas:** `sqlalchemy`, `logging`, `typing`.
- **Flujo Interno:** El servicio depende de funciones externas definidas en otros archivos (`routes.inventory.get_inventory_context`, `routes.tasks.get_tasks_context`, `routes.analytics_proyecciones.get_proyecciones_context`).

