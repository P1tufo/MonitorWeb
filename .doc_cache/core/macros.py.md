## Archivo: ./core/macros.py

### Resumen Funcional
El archivo `macros.py` centraliza reglas de negocio y macros SQL para ser utilizadas en múltiples capas de la aplicación, facilitando la expresión de lógicas complejas y reutilizables.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `AREA_EXPR` (Variable Global) - Expresión SQL que determina el área empresarial basada en los centros de costo o ubicaciones binarias.
- `EXCLUDED_USERS_INACTIVITY` (Variable Global) - Tupla con usuarios excluidos explícitamente de las métricas de inactividad.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directas.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos dentro del proyecto. Es una capa central que puede ser utilizada por cualquier otro módulo que necesite inyectar macros SQL en sus consultas.

Este archivo actúa como un punto central para la gestión y reutilización de expresiones SQL complejas y lógicas de negocio, asegurando que estas puedan ser fácilmente aplicadas en diferentes partes de la aplicación sin duplicación de código.

