## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Genera un contexto completo que incluye estadísticas de eficiencia, datos históricos y otros detalles relevantes para el dashboard de Movimientos.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `fmt_num(val)` - Formatea un número como una cadena con separadores de miles.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_get_empty_context()` - Devuelve un contexto vacío con valores por defecto.
- `get_full_context()` - Genera y devuelve el contexto completo para el dashboard de Movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:**
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación, ej. Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.state.get_cache_manager()`
  - `core.utils.sanitize_for_json()`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository(self.session)`
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno
- **Dirección del Flujo de Datos:**
  - El archivo importa datos desde la base de datos y los procesa para generar un contexto completo.
  - El contexto generado se almacena en caché para futuras solicitudes.

