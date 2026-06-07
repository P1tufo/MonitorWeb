## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica del servicio de entregas para un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar el contexto completo para las entregas, incluyendo información sobre áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context() -> Dict[str, Any]` - Genera y devuelve un contexto completo para las entregas.
  - **Propósito**: Recopila y organiza información relevante sobre áreas de negocio y widgets configurados.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`, `typing`
  
- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**:
  - Ninguno
  
- **Archivos del Proyecto que Este Archivo IMPORTA (consume)**:
  - `core.models.ConfigQuery`
  - `routes.analytics_proyecciones.get_proyecciones_context`
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`

**Flujo de Datos**: 
1. El servicio se inicializa con una sesión de base de datos.
2. Llama a `get_full_context()` para generar el contexto completo.
3. Consulta la tabla `outbound_deliveries` para obtener áreas de negocio distintas.
4. Recupera widgets configurados desde la base de datos.
5. Intenta cargar contextos adicionales desde otros módulos (`routes.analytics_proyecciones`, `routes.inventory`, `routes.tasks`) y los combina en el contexto final.

**Nota**: El archivo importa funciones desde otros archivos, lo que indica un flujo bidireccional de dependencias dentro del proyecto.

