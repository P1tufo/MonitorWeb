## Archivo: ./services/inventory_service.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene una clase `InventoryService` que proporciona métodos para calcular y preparar diversos KPIs (Indicadores Clave de Desempeño) relacionados con el inventario, incluyendo ingresos, consumos, traspasos, devoluciones y eficiencia de bodega. Utiliza una base de datos SQL para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_prepare_volume_kpis(anio, mes)` - Calcula KPIs relacionados con los volúmenes de ingresos y consumos.
- `_prepare_abc_analytics(anio, mes)` - Realiza análisis ABC para determinar el impacto de diferentes materiales en el inventario.
- `_prepare_area_analytics(anio, mes)` - Calcula estadísticas de consumo por área con promedios diarios robustos.
- `_prepare_trend_analytics(anio, mes)` - Genera tendencias de movimientos de inventario a nivel semanal y mensual.
- `_prepare_user_location_analytics(anio, mes)` - Estadísticas detalladas de usuarios y ubicaciones con actividad mensual.
- `_prepare_planned_consumption_trend()` - Calcula la tendencia de consumos planificados vs desplanificados.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `text` for SQL queries)
- Tablas:
  - `inventory_movements`
- Columnas:
  - `fe_contab`, `cmv`, `tipo_operacion`, `material`, `qty`, `registrado`, `usuario`, `alm`, `texto_cab_documento`, `referencia`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `repositories.InventoryRepository` (para obtener datos de inventario)
  - `core.utils.sanitize_for_json` (para sanitizar datos para JSON)
  - `core.state.get_app_state` (no se usa en este fragmento)
  - `core.wms_config.COST_CENTER_MAPPING` (no se usa en este fragmento)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene funciones para preparar y obtener el contexto de datos necesario para un dashboard de movimientos en una aplicación de inventario. Incluye la generación de indicadores clave (KPIs), análisis de volumen, área, ABC, usuarios, tendencias y proyecciones.

### Catálogo de Funciones y Clases
- `_prepare_planned_consumption_trend()` - Prepara los datos para el gráfico de consumo planificado.
- `_get_empty_context()` - Devuelve un contexto vacío con valores iniciales.
- `get_full_context()` - Genera el contexto completo para el dashboard, incluyendo KPIs, análisis y proyecciones.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Depende de la clase `InventoryRepository` para interactuar con la base de datos.
- Comunica con el archivo `routes.analytics_proyecciones.py` para obtener contexto de proyecciones.
- Utiliza funciones como `get_app_state()`, `set_cache()`, y `save_analytics_snapshot()` que no se muestran en el fragmento.

