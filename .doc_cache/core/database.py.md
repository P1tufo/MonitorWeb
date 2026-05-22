## Archivo: ./core/database.py

### Resumen Funcional
Este archivo define una fábrica de sesiones SQLAlchemy para interactuar con bases de datos SQLite y PostgreSQL. Proporciona funciones para obtener sesiones, realizar consultas y verificar la conectividad con la base de datos.

### Catálogo de Funciones y Clases
- `get_session()` - Devuelve un contexto manager que proporciona una sesión SQLAlchemy.
- `get_session_dep()` - Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos.

### Interacción con Base de Datos
- **Motor**: SQLAlchemy
- **Tablas**: No aplica (no se especifican tablas directamente)
- **Columnas**: No aplica (no se especifican columnas directamente)
- **Consultas SQL Crudas**: `SELECT 1` para verificar conectividad

### Estado y Variables Globales
- `DATABASE_URL`: Variable de entorno que determina el motor de base de datos a usar.
- `_DEFAULT_URL`: URL por defecto si no se especifica `DATABASE_URL`.
- `_connect_args`: Argumentos adicionales para la conexión, dependiendo del tipo de base de datos.

### Dependencias y Flujo
- **Librerías Externas**: SQLAlchemy, logging, contextlib, typing.
- **Flujo Interno**: El archivo no interactúa con otros archivos directamente. Todas las funciones son independientes entre sí.

