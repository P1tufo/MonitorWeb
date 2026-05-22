## Archivo: ./core/security.py

### Resumen Funcional
Este archivo contiene utilidades centralizadas de seguridad y validación, específicamente para prevenir SQL Injection mediante la validación del nombre de las tablas contra una lista blanca.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
- `WHITELIST_TABLES: Final[Set[str]]` - Variable global que almacena una lista blanca de tablas permitidas para evitar SQL Injection.

### Dependencias y Flujo
No depende de ninguna librería externa. No comunica con otros archivos del proyecto.

