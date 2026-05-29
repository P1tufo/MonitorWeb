## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa semántica `semantic_layer.py` proporciona una abstracción entre el frontend y la estructura física de las bases de datos. Define clases para Dimensiones, Métricas y Conjuntos de Datos (Datasets), y ofrece funciones para obtener esquemas front-end, resolver mapeos físicos y recuperar fórmulas complejas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Representa una dimensión con sus atributos.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Representa una métrica con sus atributos.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Representa un conjunto de datos compuesto por dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjuntos de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un esquema semántico para la interfaz front-end.
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física asociada con un ID de conjunto de datos.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce IDs semánticos a columnas físicas.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Recupera expresiones SQL complejas basadas en la tabla física y la agregación.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `DATASETS`: Diccionario que almacena los conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET`: Diccionario que mapea tablas físicas a IDs de conjuntos de datos.

### Dependencias y Flujo
No depende de ninguna librería externa. Comunica con otros archivos del proyecto a través de funciones públicas como `get_frontend_schema`, `resolve_dataset_physical_table`, etc.

