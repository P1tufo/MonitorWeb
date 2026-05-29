## Archivo: ./routes/consumos.py

### Resumen Funcional
El archivo `consumos.py` define dos endpoints para obtener información de los consumos (CMV 201) en función del CeCo y una lista de materiales. Utiliza FastAPI para crear las rutas, SQLAlchemy para interactuar con la base de datos y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene los consumos agrupados por material para un CeCo específico.
- `get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene qué CeCos han consumido una lista de materiales.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `session.connection()`).
- Tablas:
  - `inventory_movements`
  - `outbound_deliveries`
- Columnas:
  - `inventory_movements`: `material`, `texto_breve_material`, `cantidad`, `importe_ml`, `cmv`, `ce_coste`, `fe_contab`.
  - `outbound_deliveries`: `centro_costo`, `area_negocio`.

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `fastapi`
  - `sqlalchemy`
  - `pandas`
  - `pydantic`
  - `logging`
  - `datetime`

- Flujo de comunicación:
  - El archivo se comunica con el resto del proyecto a través de dependencias como `get_current_user` y `get_session_dep`.

