## Archivo: ./repositories/inventory.py (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
Este archivo contiene métodos para interactuar con la base de datos SQLite y obtener información sobre movimientos de inventario y consumos. Los métodos incluyen consultas históricas, del mes actual, por materiales específicos y sugerencias de reabastecimiento.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str) -> dict`: Obtiene los consumos históricos y del mes actual para un centro de costo específico.
- `get_consumos_materiales(materiales: list) -> dict`: Obtiene los consumos históricos y del mes actual para una lista de materiales.
- `get_material_trend(material: str, area_negocio: str, ceco: str) -> dict`: Obtiene el trend de un material específico por área y centro de costo.
- `check_table_exists() -> bool`: Verifica si la tabla 'inventory_movements' existe en la base de datos.
- `get_cmv_summary(cmv_type: str, plan_type: str, year: Optional[str] = None) -> list`: Obtiene un resumen de movimientos según el tipo CMV y el tipo de planificación.
- `get_cmv_area_details(cmv_type: str, plan_type: str, area: str, mes: Optional[str] = None, year: Optional[str] = None) -> list`: Obtiene detalles de los movimientos por área y centro de costo.
- `get_replenishment_suggestions(freq: str) -> dict`: Genera sugerencias de reabastecimiento basadas en la frecuencia de consumo.
- `get_replenishment_export_data() -> tuple[pd.DataFrame, pd.DataFrame]`: Exporta datos para el reabastecimiento.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: 
  - `inventory_movements`
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `mb5b_initial_stock`
- **Columnas**:
  - `inventory_movements`: material, texto_breve_material, umb, cantidad, importe_ml, cmv, fe_contab, ce_coste
  - `outbound_deliveries`: centro_costo, area_negocio
  - `config_cost_center_mapping`: center_code, business_area
  - `mb5b_initial_stock`: material, stock_inicial

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: pandas
- **Archivos del Proyecto que Importan a este Archivo**:
  - Repositorio de servicios (Services)
  - Rutas (Routes)
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core.utils.sanitize_for_json`
  - `base.BaseRepository`

El flujo de datos es desde el repositorio hacia los servicios y rutas, pasando por la base de datos SQLite para obtener y procesar los datos.

