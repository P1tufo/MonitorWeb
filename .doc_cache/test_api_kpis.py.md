## Archivo: ./test_api_kpis.py

### Resumen Funcional
El archivo `test_api_kpis.py` es un script de prueba para la API que expone los KPIs. Realiza una solicitud GET a la ruta `/api/kpis` con parámetros de filtro vacíos y verifica el estado de respuesta.

### Catálogo de Funciones y Clases
- `client.get("/api/kpis?date=&entrega=&area=&centro=&has_ots_filter=")` - Realiza una solicitud GET a la API para obtener los KPIs con parámetros de filtro vacíos.
- `print(response.status_code)` - Imprime el código de estado de la respuesta.
- `if response.status_code != 200:` - Verifica si el código de estado no es 200 y, en ese caso, imprime el contenido de la respuesta.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- `fastapi.testclient.TestClient` - Librería utilizada para realizar solicitudes a la API FastAPI.
- Comunicación con el archivo `main.py`, que contiene la definición de la aplicación FastAPI (`app`).

