## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `DeliveriesRepository` que se encarga de interactuar con la base de datos para obtener registros de entregas, aplicando un cálculo de área negócios y filtrando según criterios de retraso y año.

### Catálogo de Funciones y Clases
- **Clase:** `DeliveriesRepository` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - **Métodos:**
    - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
    - `_get_sla_threshold() -> int` - Retorna el umbral de SLA configurado en la base de datos.
    - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame` - Obtiene registros de entregas que cumplen con los criterios de retraso y año especificados.

### Interacción con Base de Datos
- **Motor:** No aplica (No hay interacción directa con bases de datos).
- **Tablas:** `outbound_deliveries`, `warehouse_tasks`, `DeliverySummary`.
- **Columnas:**
  - `outbound_deliveries`: `entrega`, `autor`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `fecha_carga`.
  - `warehouse_tasks`: `entrega`.
  - `DeliverySummary`: `entrega_id`.

### Estado y Variables Globales
- **No aplica** (No hay variables globales definidas).

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `sqlalchemy`.
- **Flujo Interno:** La clase `DeliveriesRepository` extiende de `BaseRepository` y utiliza métodos para obtener SQL personalizado, calcular el umbral de SLA y ejecutar consultas que pueden incluir un JOIN con la tabla `DeliverySummary`.

