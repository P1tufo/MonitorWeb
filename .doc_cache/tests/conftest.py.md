## Archivo: ./tests/conftest.py

### Resumen Funcional
Este archivo `conftest.py` es un archivo de configuración para pruebas unitarias en un proyecto de Sistema de Monitoreo de Almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define varias funciones de prueba que configuran y limpian la base de datos de pruebas, proporcionan clientes de prueba autenticados y gestionan el estado global para las pruebas.

### Catálogo de Funciones y Clases
- `TEST_SESSION_ID()` - Genera un identificador criptográficamente seguro para evitar colisiones.
- `session_db()` - Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas, creando las tablas necesarias y aplicando el esquema.
- `test_db(session_db)` - Proporciona aislamiento de datos entre pruebas individuales, vaciando las tablas antes de cada prueba.
- `client(test_db)` - Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión, parcheando dinámicamente 'sqlite3.connect'.
- `auth_client(client)` - Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas:
  - outbound_deliveries
  - inventory_movements
  - stock_levels
  - warehouse_tasks
  - autor_area_mapping
  - analytics_snapshots
  - auth_users
- Columnas: Se especifican explícitamente en las definiciones de las tablas.

### Estado y Variables Globales
- `TEST_SESSION_ID`: Identificador criptográficamente seguro para evitar colisiones.
- `MEMORY_DB_URI`: URI de la base de datos SQLite en memoria compartida.

### Dependencias y Flujo
- Librerías externas: `os`, `secrets`, `pathlib`, `sqlite3`, `unittest.mock`, `pytest`, `fastapi.testclient`.
- Archivos del proyecto que este archivo importa:
  - `config`
  - `app`
  - `core.db_config_manager`
  - `core.auth`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo configura y limpia la base de datos de pruebas, proporciona clientes de prueba autenticados y gestiona el estado global para las pruebas.

