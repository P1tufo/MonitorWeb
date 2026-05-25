## Archivo: ./repositories/deliveries.py

### Resumen Funcional
Este archivo define un repositorio para el dominio de Entregas (outbound_deliveries), que utiliza consultas SQL personalizadas y una expresión segura para determinar el área empresarial.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas.
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Obtiene el umbral de SLA (Service Level Agreement).

### Interacción con Base de Datos
- Motor de BD: No especificado.
- Tablas y Columnas: No aplica.

### Estado y Variables Globales
- `AREA_EXPR` - Expresión segura para determinar el área empresarial, definida como una constante de clase.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `sqlalchemy`
- Flujo hacia otros archivos del proyecto: No aplica.

