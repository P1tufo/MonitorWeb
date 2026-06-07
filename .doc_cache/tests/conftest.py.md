## Archivo: ./tests/conftest.py

### Resumen Funcional
Este archivo `conftest.py` es un archivo de configuración para pruebas unitarias en un proyecto de Sistema de Monitoreo de Almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define varias funciones de prueba que configuran la base de datos de pruebas, proporcionan clientes de prueba autenticados y aseguran el aislamiento entre las pruebas individuales.

### Catálogo de Funciones y Clases
- `skip_warmup()` - Desactiva un parche que fallaba durante el arranque.
- `session_db()` - Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas, incluyendo la creación de tablas y el esquema.
- `test_db(session_db)` - Proporciona aislamiento de datos entre pruebas individuales, vaciando las tablas antes de cada prueba.
- `client(test_db)` - Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión.
- `auth_client(client)` - Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `autor_area_mapping`
  - `analytics_snapshots`
  - `auth_users`
- **Columnas**: Cada tabla tiene varias columnas, pero no se detalla cada una aquí.

### Estado y Variables Globales
- `TEST_SESSION_ID`: Identificador criptográficamente seguro para evitar colisiones.
- `MEMORY_DB_URI`: URI de la base de datos SQLite en memoria compartida.
- `os.environ["DATABASE_URL"]`: URL de la base de datos configurada para pruebas.
- `os.environ["TESTING"]`: Variable de entorno indicando que se está ejecutando un entorno de prueba.

### Dependencias y Flujo
- **Librerías Externas**: `secrets`, `sys`, `pathlib`, `sqlite3`, `unittest.mock`, `pytest`, `fastapi.testclient`.
- **Archivos del Proyecto Importados**:
  - `config`
  - `app`
  - `core.auth.init_auth_db`
  - `core.db_config_manager.init_config_db`
  - `core.db_config_manager.seed_initial_config`
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**:
  - El archivo configura la base de datos de pruebas en memoria y proporciona clientes de prueba para interactuar con ella.
  - Las pruebas individuales utilizan el cliente autenticado para realizar operaciones en el sistema.

