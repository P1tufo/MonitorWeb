## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica del servicio de inventario, que se encarga de generar el contexto necesario para un dashboard de movimientos en una aplicación SaaS. El servicio interactúa con una base de datos SQL y utiliza ORM SQLAlchemy.

### Catálogo de Funciones y Clases
- **InventoryService(session: Session)** - Inicializa el servicio con una sesión de base de datos.
- **fmt_num(val)** - Formatea un número para mostrarlo como una cadena con separadores de miles.
- **_get_latest_data_period()** - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- **_get_empty_context()** - Devuelve un contexto vacío con valores por defecto.
- **get_full_context()** - Genera el contexto completo para el dashboard, incluyendo el período más reciente y otros datos relevantes.

### Interacción con Base de Datos
- **Motor**: SQLAlchemy ORM
- **Tablas**: `inventory_movements`
- **Columnas**: `fe_contab`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `sqlalchemy`, `pandas`, `logging`, `datetime`, `typing`
- **Flujo Interno**: El servicio interactúa con el repositorio de inventario para verificar la existencia de la tabla, obtiene el período más reciente de datos y genera un contexto completo.

