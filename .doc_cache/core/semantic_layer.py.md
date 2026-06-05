## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa `semantic_layer.py` proporciona una abstracción semántica sobre el esquema físico de la base de datos, manteniendo un catálogo de conjuntos de datos (datasets), dimensiones y métricas. Ofrece funciones para resolver mapeos entre IDs semánticos y físicos, generar esquemas frontend, y recuperar fórmulas complejas de métricas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Define una dimensión con su ID, etiqueta, columna física y tipo.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Define una métrica con su ID, etiqueta, columna física, agregación y fórmula compleja si es necesario.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Define un conjunto de datos con su ID, etiqueta, tabla física y listas de dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjuntos de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un diccionario semántico para exponer a la UI (Studio).
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Reverse-lookup para obtener la expresión SQL real basada en la tabla física y la agregación.

### Interacción con Base de Datos
No se utiliza ninguna base de datos explícita. Todas las operaciones relacionadas con la BD son indirectas a través de los mapeos y consultas que utilizan los IDs semánticos.

### Estado y Variables Globales
- `DATASETS: Dict[str, Dataset]` - Almacena el catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjuntos de datos.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas adicionales.
- **Flujo de Datos**:
  - `get_frontend_schema()` genera un esquema semántico para la UI.
  - `resolve_dataset_physical_table(dataset_id: str)` resuelve el mapeo entre IDs de conjuntos de datos y tablas físicas.
  - `resolve_physical_mapping(dataset_id: str, field_id: str)` traduce IDs semánticos a columnas físicas.
  - `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "")` recupera fórmulas complejas de métricas.
  - `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "")` realiza un reverse-lookup para obtener expresiones SQL basadas en tablas físicas y agregaciones.

