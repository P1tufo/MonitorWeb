## Archivo: ./core/security.py

### Resumen Funcional
Este archivo contiene utilidades centralizadas de seguridad y validación, específicamente para validar el nombre de tablas en operaciones relacionales con la base de datos.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra una lista blanca predefinida para evitar SQL Injection.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (La validación se realiza en memoria, no hay consultas a la base de datos).
- **Columnas**: Ninguna

### Estado y Variables Globales
- `WHITELIST_TABLES: Final[Set[str]]` - Variable global que almacena una lista blanca de tablas permitidas.

### Dependencias y Flujo
- **Dependencias Externas**: No hay dependencias externas.
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Repositories, Services o cualquier otro componente que necesite validar el nombre de las tablas.

**Flujo de Datos**: El archivo `security.py` se importa en otros componentes del sistema para validar el nombre de las tablas antes de realizar operaciones relacionales con la base de datos.

