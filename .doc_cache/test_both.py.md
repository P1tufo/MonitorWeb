## Archivo: ./test_both.py

### Resumen Funcional
El archivo `test_both.py` es un script de prueba que ejecuta funciones para filtrar transacciones y obtener KPIs en una área específica ("ASERRADERO"). Utiliza una sesión de base de datos para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `run()` - Ejecuta las pruebas para `filter_transactions` y `get_kpis`, imprimiendo el número de resultados obtenidos.
- `filter_transactions(request=None, area="ASERRADERO", session=SessionLocal())` - Filtra transacciones en una área específica.
- `get_kpis(area="ASERRADERO", session=SessionLocal())` - Obtiene KPIs para una área específica.

### Interacción con Base de Datos
- Motor: No especificado (se espera que `SessionLocal()` configure el motor).
- Tablas y Columnas: No se mencionan explícitamente, pero se asume que interactúa con tablas relacionadas con transacciones y KPIs.
- Consultas SQL Crudas o ORM: Se espera que las funciones `filter_transactions` y `get_kpis` utilicen consultas SQL o ORM para acceder a la base de datos.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías Externas:
  - `asyncio`
  - `sys`
- Comunicación con otros archivos del proyecto:
  - Importa funciones desde `core.database` y `routes.filters`.

El script se ejecuta directamente si es el archivo principal, iniciando una sesión de base de datos y ejecutando las pruebas asincrónicas para filtrar transacciones y obtener KPIs.

