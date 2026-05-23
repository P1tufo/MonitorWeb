## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene funciones para filtrar y calcular KPIs basados en múltiples criterios. Ofrece endpoints para obtener datos filtrados de entregas y calcular indicadores clave de rendimiento (KPIs) dinámicos.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str)` - Construye la cláusula WHERE a nivel de MATERIAL con seguridad contra SQL Injection.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios y devuelve los resultados como un DataFrame.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.

### Interacción con Base de Datos
- Motor de BD: No especificado.
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
- Columnas:
  - `outbound_deliveries`: `entrega`, `fecha_carga`, `fecha_sm_real`, `creado_el`, `estado_wms`, `material`, `dias_retraso`.
  - `config_cost_center_mapping`: `center_code`, `business_area`.

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy`
  - `pandas`
  - `fastapi`
- Comunicación con otros archivos del proyecto:
  - Depende de `core.database.get_session_dep` para obtener una sesión de base de datos.

