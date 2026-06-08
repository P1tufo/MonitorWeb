## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa `semantic_layer.py` proporciona una abstracción semántica sobre el esquema físico de la base de datos, permitiendo que el frontend acceda a los conjuntos de datos (datasets), dimensiones y métricas mediante identificadores semánticos en lugar de nombres físicos de tablas o columnas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Define una dimensión con su identificador, etiqueta, columna física y tipo.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Define una métrica con su identificador, etiqueta, columna física, agregación y fórmula compleja si es necesario.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Define un conjunto de datos con su identificador, etiqueta, tabla física y listas de dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a sus respectivos conjuntos de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un diccionario semántico para exponer a la UI (Studio).
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Reverse-lookup para obtener la expresión SQL real basada en la tabla física y la agregación.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Columnas:
  - `area_negocio` (en `outbound_deliveries`)
  - `fecha_carga` (en `outbound_deliveries`)
  - `material` (en varias tablas)
  - `estado_wms` (en `outbound_deliveries`)
  - `centro_costo` (en varias tablas)
  - `autor` (en `outbound_deliveries`)
  - `entrega` (en `outbound_deliveries`)
  - `dias_retraso` (en varias tablas)
  - `cantidad` (en varias tablas)
  - `stock_disp` (en `stock_levels`)
  - `fe_creac` (en `warehouse_tasks`)
  - `fecha_conf` (en `warehouse_tasks`)
  - `numero_ot` (en `warehouse_tasks`)
  - `ctd_teor_dsd` (en `warehouse_tasks`)
  - `fe_contab` (en varias tablas)
  - `ce_coste` (en `inventory_movements`)
  - `cmv` (en varias tablas)
  - `tipo_operacion` (en varias tablas)
  - `texto_cab_documento` (en varias tablas)

### Estado y Variables Globales
- `DATASETS: Dict[str, Dataset]` - Almacena el catálogo de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a sus respectivos conjuntos de datos.

### Dependencias y Flujo
- Librerías externas: `dataclasses`, `typing`.
- Archivos del proyecto que importan a este archivo:
  - `services.py`
  - `repositories.py`
  - `db.py`
- Archivos del proyecto que este archivo importa:
  - Ninguno

El flujo de datos es unidireccional, con el archivo `semantic_layer.py` proporcionando funciones para obtener información semántica y mapeos entre IDs semánticos y físicos.

