## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa `semantic_layer.py` es una implementación de la Capa Semántica en un sistema de monitoreo de almacén (WMS) basado en FastAPI, SQLAlchemy y SQLite. Esta capa se encarga de aislar el frontend del esquema físico de la base de datos, proporcionando un diccionario semántico que incluye los conjuntos de datos, dimensiones y métricas con sus respectivas fórmulas de negocio.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "") -> None`: Define una dimensión del esquema semántico.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "") -> None`: Define una métrica del esquema semántico.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list)) -> None`: Define un conjunto de datos que incluye dimensiones y métricas.

### Contratos de API / Endpoints
No aplica. El archivo no define rutas HTTP.

### Interacción con Base de Datos
- **Tabla afectada**: `outbound_deliveries`, `stock_levels`, `warehouse_tasks`, `inventory_movements`
- **Tipo de operación**: No aplica (no hay consultas SQL directas en este archivo).
- **Columnas leídas o escritas**: Todas las columnas definidas en las dimensiones y métricas.
- **JOINs o subqueries relevantes**: No aplica.

### Flujo de Datos y Pipeline
No aplica. El archivo no procesa, transforma ni mueve datos.

### Caché y Estado
- **Variables globales y de módulo**: `DATASETS`, `_PHYSICAL_TABLE_TO_DATASET`
- **Caché en memoria**: No aplica.
- **Caché persistente**: No aplica.
- **Mecanismos de invalidación de caché**: No aplica.
- **Variables de entorno o sesión utilizadas**: No aplica.

### Lógica de Negocio y Reglas
- **Diccionarios o mapeos hardcoded**:
  - `DATASETS`: Contiene los conjuntos de datos, dimensiones y métricas con sus respectivas fórmulas.
  - `_PHYSICAL_TABLE_TO_DATASET`: Mapeo inverso de tablas físicas a IDs de conjunto de datos.

- **Constantes de negocio o umbrales**:
  - No aplica (excepto en las fórmulas de métrica).

- **Fórmulas de cálculo o reglas de validación**:
  - Todas las fórmulas de métrica están definidas dentro del diccionario `DATASETS`.

### Dependencias y Flujo
- **Librerías externas**: No aplica.
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: No aplica.
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: No aplica.

