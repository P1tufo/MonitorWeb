## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene métodos para obtener datos de inventario, específicamente consumos y tendencias de materiales. Utiliza SQLAlchemy para interactuar con una base de datos SQLite.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str) -> dict`: Obtiene los consumos históricos y del mes actual por centro de costo (CeCo).
- `get_consumos_materiales(materiales: list) -> dict`: Obtiene los consumos históricos y del mes actual para una lista de materiales.
- `get_material_trend(material: str, area_negocio: str, ceco: str) -> dict`: Obtiene la tendencia de un material específico por área de negocio y centro de costo (CeCo).
- `check_table_exists() -> bool`: Verifica si la tabla `inventory_movements` existe en la base de datos.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: 
  - `inventory_movements`
  - `outbound_deliveries`
- **Columnas**:
  - `inventory_movements`: `material`, `texto_breve_material`, `umb`, `cantidad`, `importe_ml`, `cmv`, `fe_contab`, `hora`, `ce_coste`
  - `outbound_deliveries`: `centro_costo`, `area_negocio`

### Estado y Variables Globales
- **Variables Globales**: Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `pandas`
  - `sqlalchemy`
  - `datetime`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**:
  - El archivo importa `BaseRepository` desde el módulo `.base`.
  - Utiliza `pandas` para procesar los resultados de las consultas SQL.
  - Realiza consultas SQL directamente en la base de datos SQLite utilizando SQLAlchemy.

