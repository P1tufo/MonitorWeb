## Archivo: ./core/macros.py

### Resumen Funcional
El archivo `macros.py` centraliza reglas de negocio y macros SQL para ser utilizadas en múltiples capas de la aplicación, facilitando la expresión de lógicas complejas que deben inyectarse en el código SQL.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa sobre la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: Ninguna.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos dentro del proyecto. No hay interacción con otras partes del sistema a través de funciones o clases.

