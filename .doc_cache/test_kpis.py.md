## Archivo: ./test_kpis.py

### Resumen Funcional
El archivo `test_kpis.py` es un script que ejecuta una función para obtener KPIs (Indicadores Clave de Desempeño) utilizando una sesión de base de datos y luego imprime los resultados.

### Catálogo de Funciones y Clases
- `run()` - Asincrónica, inicia una sesión de base de datos, ejecuta la función `get_kpis` para obtener KPIs, e imprime el resultado o cualquier error que ocurra.

### Interacción con Base de Datos
- Motor: SQLAlchemy (implícito a través de `SessionLocal`)
- Tablas y Columnas: No se especifican explícitamente en el fragmento proporcionado.
- Consultas SQL Crudas/ORM: Se hace uso de una función llamada `get_kpis` que probablemente realiza consultas ORM para obtener los KPIs.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías Externas:
  - `asyncio`
  - `sqlalchemy`
- Comunicación con otros archivos del proyecto:
  - Importa `SessionLocal` desde `core.database`
  - Importa `get_kpis` desde `routes.filters`

Este archivo es un ejemplo de cómo se pueden realizar pruebas asincrónicas para obtener y mostrar datos utilizando una base de datos a través de SQLAlchemy.

