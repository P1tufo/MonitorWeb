## Auditoría Global de Software y Deuda Técnica

### 1. Funciones Duplicadas o Solapadas

**Función Duplicada:**
- **Ubicación:** `core/pdf_queries.py` y `core/db_config_manager.py`

**Descripción:**
Ambos archivos contienen una función llamada `get_outbound_deliveries_query()` que ejecuta la misma consulta SQL para obtener los registros de entregas.

```python
# core/pdf_queries.py
def get_outbound_deliveries_query():
    return "SELECT * FROM outbound_deliveries"

# core/db_config_manager.py
def get_outbound_deliveries_query():
    return "SELECT * FROM outbound_deliveries"
```

**Recomendación:**
Crear un archivo `utils.py` y mover la función allí para evitar duplicidad.

```python
# utils.py
def get_outbound_deliveries_query():
    return "SELECT * FROM outbound_deliveries"
```

### 2. Inconsistencias en Base de Datos

**Inconsistencia:**
- **Ubicación:** `core/db_config_manager.py` y `core/pdf_queries.py`

**Descripción:**
Ambos archivos utilizan consultas SQL crudas para interactuar con la base de datos, lo que puede llevar a inconsistencias si las tablas cambian.

```python
# core/db_config_manager.py
def create_table():
    query = "CREATE TABLE IF NOT EXISTS outbound_deliveries (id INTEGER PRIMARY KEY)"

# core/pdf_queries.py
def get_outbound_deliveries_query():
    return "SELECT * FROM outbound_deliveries"
```

**Recomendación:**
Utilizar ORM SQLAlchemy para evitar consultas SQL crudas y mantener la consistencia.

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class OutboundDelivery(Base):
    __tablename__ = 'outbound_deliveries'
    id = Column(Integer, primary_key=True)

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()
```

### 3. Riesgos de Estado Global

**Estado Global:**
- **Ubicación:** `core/state.py`

**Descripción:**
El archivo `state.py` contiene una variable global llamada `AppState`, que podría ser un riesgo si no se gestiona adecuadamente.

```python
# core/state.py
class AppState:
    def __init__(self):
        self.is_syncing = False

app_state = AppState()
```

**Recomendación:**
Utilizar inyección de dependencias para gestionar el estado global y evitar variables globales.

```python
from fastapi import Depends, FastAPI

app = FastAPI()

class AppState:
    def __init__(self):
        self.is_syncing = False

@app.get("/")
async def read_root(app_state: AppState = Depends()):
    return {"is_syncing": app_state.is_syncing}
```

### 4. Veredicto de Refactorización

**Archivos Problematicos:**
1. **`core/db_config_manager.py`:** Utiliza consultas SQL crudas y no utiliza ORM SQLAlchemy.
2. **`core/pdf_queries.py`:** Contiene funciones duplicadas y utiliza consultas SQL crudas.
3. **`core/state.py`:** Utiliza una variable global para gestionar el estado del sistema.

**Razones:**
- `core/db_config_manager.py` necesita ser refactorizado para utilizar ORM SQLAlchemy, lo que mejora la consistencia y seguridad de las operaciones con la base de datos.
- `core/pdf_queries.py` tiene funciones duplicadas y utiliza consultas SQL crudas, lo que dificulta el mantenimiento y aumenta el riesgo de errores.
- `core/state.py` utiliza una variable global para gestionar el estado del sistema, lo que puede llevar a problemas de inmutabilidad y dificultad en la gestión del estado.

**Recomendación:**
Refactorizar estos archivos primero para mejorar la calidad y mantenibilidad del código.

