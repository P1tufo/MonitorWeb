## Archivo: ./test_filter.py

### Resumen Funcional
El archivo `test_filter.py` es un script de prueba que ejecuta una función para filtrar transacciones en la base de datos y muestra los resultados.

### Catálogo de Funciones y Clases
- `run()` - Ejecuta la función `filter_transactions` con parámetros específicos y maneja la sesión de la base de datos.

### Interacción con Base de Datos
- Motor: No aplica (el archivo no interactúa directamente con una base de datos).
- Tablas y Columnas: No aplica (no hay consultas SQL ni interacciones con tablas).

### Estado y Variables Globales
- No aplica (no se definen variables globales, de sesión o diccionarios quemados en el código).

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sys` - Para manipular los parámetros del sistema.
  - `asyncio` - Para manejar la ejecución asíncrona.
- Comunicación con otros archivos:
  - Importa `SessionLocal` desde `core.database`.
  - Importa `filter_transactions` desde `routes.filters`.

