## Auditoría Global de Software y Deuda Técnica

### 1. Funciones Duplicadas o Solapadas

**Funciones Duplicadas:**
- **`core.query_engine.build_query_from_payload`**: Esta función parece estar definida en varios archivos como `core/query_engine.py`, `core/database.py`, y `app.py`. Debería ser movida a un archivo compartido, por ejemplo, `utils/helpers.py`.

**Sugerencia de Refactorización:**
- Crear un archivo `utils/helpers.py` y mover la función `build_query_from_payload` allí.
- Importar la función desde `utils.helpers` en los archivos donde se utiliza.

### 2. Inconsistencias en Base de Datos

**Inconsistencias en Consultas SQL:**
- **`core.database.get_user_by_email`**: Esta función parece estar definida en varios archivos como `core/database.py`, `app.py`, y `core/auth.py`. Debería ser unificado para evitar inconsistencias.
- **`core.query_engine.execute_query`**: Similarmente, esta función también está definida en múltiples archivos. Debería ser movida a un archivo compartido.

**Sugerencia de Refactorización:**
- Crear un archivo `utils/database_utils.py` y mover las funciones relacionadas con la base de datos allí.
- Importar las funciones desde `utils.database_utils` en los archivos donde se utiliza.

### 3. Riesgos de Estado Global

**Variables Globales:**
- **`fastapi_app.state.global_state`**: Esta variable global está definida en varios archivos como `app.py`, `core/auth.py`, y `core/database.py`. Debería ser eliminada y almacenada en la base de datos o en variables de entorno `.env`.

**Sugerencia de Refactorización:**
- Eliminar el uso de `fastapi_app.state.global_state`.
- Almacenar el estado global en la base de datos utilizando SQLAlchemy.
- Utilizar variables de entorno `.env` para configuraciones estáticas.

### 4. Veredicto de Refactorización

**3 Archivos Más Problemáticos:**
1. **`app.py`**: Este archivo contiene la inicialización del servidor FastAPI y la configuración global, lo que hace que sea un punto central de problemas.
2. **`core/database.py`**: Este archivo contiene múltiples funciones relacionadas con la base de datos, lo que dificulta su mantenimiento y escalabilidad.
3. **`core/query_engine.py`**: Este archivo contiene funciones para construir consultas SQL dinámicas, lo que puede llevar a inconsistencias y problemas de seguridad.

**Razones:**
- **`app.py`**: Es el punto central del sistema y es donde se configuran todas las dependencias. Si hay problemas aquí, pueden afectar toda la aplicación.
- **`core/database.py`**: Contiene múltiples funciones relacionadas con la base de datos, lo que dificulta su mantenimiento y escalabilidad. Además, si hay inconsistencias en las consultas SQL, pueden llevar a problemas de seguridad.
- **`core/query_engine.py`**: Contiene funciones para construir consultas SQL dinámicas, lo que puede llevar a inconsistencias y problemas de seguridad. Además, si hay problemas aquí, pueden afectar la funcionalidad del sistema.

**Sugerencia de Refactorización:**
- Crear un archivo `utils/database_utils.py` y mover las funciones relacionadas con la base de datos allí.
- Importar las funciones desde `utils.database_utils` en los archivos donde se utiliza.
- Eliminar el uso de `fastapi_app.state.global_state`.
- Almacenar el estado global en la base de datos utilizando SQLAlchemy.
- Utilizar variables de entorno `.env` para configuraciones estáticas.

