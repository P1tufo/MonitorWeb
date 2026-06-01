## Archivo: ./core/security.py

### Resumen Funcional
Utilidades centralizadas de seguridad y validación, específicamente para validar el nombre de tablas contra una lista blanca para prevenir SQL Injection.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection. Lanza `ValueError` si la tabla no está permitida.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- Motor: SQLite
- Operación: SELECT (implicada en la validación)
- Tabla afectada: Todas las tablas mencionadas en `WHITELIST_TABLES`
- Columnas leídas: Nombre de la tabla

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo:
  - `WHITELIST_TABLES`: Conjunto inmutable de nombres de tablas permitidas.

### Lógica de Negocio y Reglas
- Constantes de negocio o umbrales:
  - `WHITELIST_TABLES`: Lista blanca de tablas permitidas para evitar SQL Injection.

### Dependencias y Flujo
- Librerías externas: `typing`
- Archivos del proyecto que IMPORTA a este archivo (lo consumen): No aplica.
- Archivos del proyecto que este archivo IMPORTA (consume): No aplica.

