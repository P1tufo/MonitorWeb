## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa semántica `semantic_layer.py` mantiene el catálogo de conjuntos de datos (datasets), dimensiones y métricas, junto con sus fórmulas de negocio. Proporciona funciones para obtener esquemas front-end, resolver mapeos físicos y recuperar fórmulas complejas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Define una dimensión con sus atributos.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Define una métrica con sus atributos.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Define un conjunto de datos con sus dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjunto de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un diccionario semántico para exponer a la UI (Studio).
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Reverse-lookup para obtener la expresión SQL real dada una tabla física y una agregación compleja.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `DATASETS: Dict[str, Dataset]` - Almacena el catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjunto de datos.

### Dependencias y Flujo
- **Dependencias**: No importa ninguna librería externa.
- **Flujo de Datos**:
  - `get_frontend_schema()` consume `DATASETS` y genera un esquema semántico para la UI.
  - `resolve_dataset_physical_table(dataset_id: str)` consume `DATASETS`.
  - `resolve_physical_mapping(dataset_id: str, field_id: str)` consume `DATASETS`.
  - `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "")` consume `DATASETS`.
  - `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "")` consume `_PHYSICAL_TABLE_TO_DATASET` y `DATASETS`.

