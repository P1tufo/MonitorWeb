## Archivo: ./services/inventory_service.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene una clase `InventoryService` que proporciona métodos para calcular y preparar diversos KPIs (Indicadores Clave de Desempeño) relacionados con el inventario. Estos KPIs incluyen ingresos, consumos, traspasos, devoluciones, eficiencia de bodega, análisis ABC, estadísticas por área y tendencias de consumo planificado vs desplanificado.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_prepare_volume_kpis(anio, mes)` - Calcula KPIs relacionados con el volumen de movimientos de inventario.
- `_prepare_abc_analytics(anio, mes)` - Realiza análisis ABC para determinar la importancia relativa de los materiales según su consumo.
- `_prepare_area_analytics(anio, mes)` - Calcula estadísticas de consumo por área.
- `_prepare_trend_analytics(anio, mes)` - Genera tendencias de consumo a nivel semanal y mensual.
- `_prepare_user_location_analytics(anio, mes)` - Analiza la actividad de usuarios y ubicaciones según el inventario.
- `_prepare_planned_consumption_trend()` - Calcula la tendencia de consumos planificados vs desplanificados.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `Session` and `text`)
- Tablas:
  - `inventory_movements`
- Columnas:
  - `fe_contab`
  - `tipo_operacion`
  - `material`
  - `cmv`
  - `usuario`
  - `alm`
  - `texto_cab_documento`
  - `referencia`
  - `registrado`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `typing`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `repositories.InventoryRepository` (se importa y se usa para obtener datos)
  - `core.utils.sanitize_for_json` (se importa y se usa para sanitizar datos JSON)
  - `core.state.get_app_state` (se importa pero no se usa en el fragmento proporcionado)
  - `core.wms_config.COST_CENTER_MAPPING` (se importa pero no se usa en el fragmento proporcionado)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene funciones para preparar y obtener el contexto de datos necesario para un dashboard de movimientos en una aplicación de inventario. Incluye la generación de indicadores clave (KPIs), análisis de volumen, área, ABC, usuarios, tendencias, proyecciones, mapeos detallados y gráficos planificados vs desplanificados.

### Catálogo de Funciones y Clases
- `_prepare_planned_consumption_trend()` - Prepara los datos para el gráfico de tendencia de consumo planificado.
- `_get_empty_context()` - Devuelve un contexto vacío con valores iniciales.
- `get_full_context()` - Genera el contexto completo para el dashboard de movimientos, incluyendo KPIs, análisis y mapeos.

### Interacción con Base de Datos
El archivo interactúa con una base de datos a través del repositorio `InventoryRepository`. Las tablas y columnas específicas no se mencionan explícitamente en el código proporcionado. Sin embargo, se hacen llamadas a métodos como `check_table_exists()`, `get_location_material_summary()`, `get_area_material_mapping_201()`, `get_user_material_mapping()`, `get_pm_type_material_records()` y otras que implican la lectura de datos.

### Estado y Variables Globales
No aplica. El código no define variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas en el fragmento proporcionado.
- **Flujo Interno**: El archivo interactúa con otros archivos del proyecto a través de llamadas como `get_proyecciones_context()` y `save_analytics_snapshot()`.

