## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Genera un contexto completo que incluye estadísticas de eficiencia, datos históricos y otros detalles relevantes para el dashboard de movimientos.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `fmt_num(val)` - Formatea un número como una cadena con separadores de miles.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_get_empty_context()` - Devuelve un contexto vacío con valores por defecto.
- `get_full_context()` - Genera y devuelve el contexto completo para el dashboard de movimientos.

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
  - `repositories.InventoryRepository`
  - `core.utils.sanitize_for_json`
  - `core.state.get_app_state`
  - `core.wms_config.COST_CENTER_MAPPING`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

**Flujo de Datos:**
1. El archivo se importa y se utiliza en el servicio principal.
2. Se inicia una sesión de base de datos (`InventoryService`).
3. Se ejecutan consultas SQL para obtener los datos necesarios.
4. Los resultados son procesados y formateados usando `pandas`.
5. El contexto completo es generado y almacenado en caché.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando las estadísticas y datos necesarios para el análisis y visualización de los movimientos de inventario.

