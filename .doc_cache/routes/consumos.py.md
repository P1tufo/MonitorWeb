## Archivo: ./routes/consumos.py

### Resumen Funcional
El archivo `consumos.py` define endpoints para obtener datos de consumos (CMV 201) desde una base de datos relacionada con movimientos de inventario. Los endpoints permiten consultar los consumos históricos y actuales por CeCo, así como el consumo mensual de materiales específicos.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene los consumos históricos y actuales por CeCo.
- `get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene el consumo de materiales específicos.
- `get_material_trend(req: MaterialTrendRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Devuelve el consumo mensual de un material específico, filtrado por área de negocio.

### Interacción con Base de Datos
- **Motor:** PostgreSQL (deducido del uso de `sqlalchemy.text`)
- **Tablas:** `inventory_movements`, `outbound_deliveries`
- **Columnas:**
  - `inventory_movements`: `doc_mat`, `ej_mat`, `pos`, `material`, `texto_breve_material`, `umb`, `cantidad`, `importe_ml`, `cmv`, `fe_contab`, `hora`, `ce_coste`
  - `outbound_deliveries`: `centro_costo`, `area_negocio`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- **Librerías Externas:** `fastapi`, `sqlalchemy`, `pandas`, `pydantic`
- **Flujo Interno:** El archivo interactúa con el resto del proyecto a través de dependencias como `get_current_user` y `get_session_dep`.

