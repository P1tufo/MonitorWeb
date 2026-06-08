## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Define una clase `InventoryService` que interactúa con la base de datos para obtener y procesar datos de movimientos de inventario, calculando estadísticas de eficiencia y generando un contexto completo para el dashboard.

### Catálogo de Funciones y Clases
- **Clase: InventoryService**
  - **Método:** `__init__(self, session: Session)`
    - **Propósito:** Inicializa la instancia con una sesión de base de datos.
  
  - **Método:** `fmt_num(self, val)`
    - **Propósito:** Formatea un número para mostrarlo como una cadena con separadores de miles y decimales.

  - **Método:** `_get_latest_data_period(self) -> Tuple[str, str]`
    - **Propósito:** Obtiene el período más reciente de datos disponibles en la base de datos.

  - **Método:** `_get_empty_context(self) -> Dict[str, Any]`
    - **Propósito:** Devuelve un contexto vacío con valores por defecto para las estadísticas y métricas del inventario.

  - **Método:** `get_full_context(self) -> Dict[str, Any]`
    - **Propósito:** Genera el contexto completo para el dashboard de Movimientos (Fase 3: SaaS), incluyendo estadísticas de eficiencia y datos históricos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación: Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:** 
  - `pandas`
  - `numpy`
  - `sqlalchemy`

- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.InventoryRepository`

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.cache_decorator.analytics_cache`
  - `core.state.get_cache_manager`
  - `core.utils.sanitize_for_json`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository`

**Flujo de Datos:** 
1. El archivo se importa por otros archivos del proyecto.
2. Se crea una instancia de `InventoryService` pasando una sesión de base de datos.
3. Llama al método `get_full_context()` para generar el contexto completo.
4. Este método interactúa con la base de datos para obtener y procesar los datos necesarios.
5. Los resultados se almacenan en caché para mejorar el rendimiento.

Este archivo es crucial para el funcionamiento del sistema de gestión de inventario, proporcionando las estadísticas y datos necesarios para el dashboard de Movimientos.

