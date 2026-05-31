## Archivo: ./core/security.py

### Resumen Funcional
Este archivo contiene utilidades centralizadas de seguridad y validación, específicamente para prevenir SQL Injection mediante la validación del nombre de las tablas contra una lista blanca.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection.

### Interacción con Base de Datos
- **Motor:** No aplica.
- **Tablas:** No aplica.
- **Columnas:** No aplica.

### Estado y Variables Globales
- `WHITELIST_TABLES: Final[Set[str]]` - Variable global que almacena una lista blanca de tablas permitidas para evitar SQL Injection.

### Dependencias y Flujo
- **Librerías Externas:** `typing`
- **Flujo Interno:** La función `validate_table` utiliza la variable global `WHITELIST_TABLES` para validar el nombre de la tabla proporcionado.

