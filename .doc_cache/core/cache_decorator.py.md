## Archivo: ./core/cache_decorator.py

### Resumen Funcional
El archivo `cache_decorator.py` contiene funciones y un decorador para implementar una caché multinivel en un sistema de monitoreo de almacén (WMS). El decorador permite almacenar y recuperar datos analíticos tanto en memoria como en una base de datos SQLite, utilizando un patrón de caché que prioriza la velocidad de acceso a los datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics_cache(key_prefix: str)` - Decorador que implementa el patrón de caché multinivel (Memoria -> DB Snapshot -> Cálculo).

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `analytics_snapshots`
    - Columnas:
      - `key` (TEXT, PRIMARY KEY)
      - `data` (TEXT)
      - `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `json`, `logging`, `datetime`, `functools`, `typing`
- Archivos del proyecto que IMPORTA:
  - `core.state` (para `get_cache_manager`)
- Archivos del proyecto que IMPORTAN a este archivo:
  - Ninguno

**Flujo de Datos:**
1. **Entrada:** Llamada al método decorado con parámetros.
2. **Proceso:**
   - Verifica si existe una sesión (`self.session`).
   - Genera claves para caché en memoria y base de datos.
   - Intenta recuperar los datos desde la caché en memoria.
   - Si no está en caché, intenta recuperarlos desde el snapshot en la base de datos.
   - Si no están disponibles, ejecuta el cálculo completo del método decorado.
   - Almacena los resultados en la caché en memoria y en la base de datos si es un diccionario.
3. **Salida:** Devuelve los datos recuperados o calculados.

Este flujo asegura que los datos sean recuperados lo más rápido posible, utilizando el caché en memoria como primer recurso, seguido del snapshot en la base de datos, y finalmente ejecutando el cálculo completo si es necesario.

