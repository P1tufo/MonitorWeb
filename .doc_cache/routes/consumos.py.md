## Archivo: ./routes/consumos.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de consumos en un sistema de almacén (WMS) utilizando FastAPI. Permite consultar los consumos agrupados por material y ceco, así como el consumo mensual de materiales específicos.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene los consumos agrupados por material para un CeCo específico.
- `get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene que CeCos han consumido una lista de materiales.
- `get_material_trend(req: MaterialTrendRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Devuelve el consumo mensual de un material específico, filtrado por área de negocio.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
- Columnas:
  - `doc_mat`, `ej_mat`, `pos`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `fastapi`
  - `pydantic`
  - `sqlalchemy`
- Archivos del proyecto que este archivo importa:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `repositories.inventory.InventoryRepository`
- Archivos del proyecto que importan a este archivo:
  - Ninguno

El flujo de datos es desde los endpoints hasta el repositorio, donde se realizan las consultas a la base de datos.

