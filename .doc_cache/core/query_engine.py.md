## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo actúa como una fachada para el motor de SQL en un sistema de monitoreo de almacén (WMS). Proporciona funciones para construir consultas SQL a partir de payloads y validar identificadores.

### Catálogo de Funciones y Clases
- `build_sql_from_payload(payload)` - Construye una consulta SQL a partir del payload proporcionado.
- `extract_metric_value(metric_name, visual_state)` - Extrae el valor de una métrica específica del estado visual.
- `get_bound_params_from_visual_state(visual_state)` - Obtiene los parámetros limitados desde el estado visual.
- `validate_identifier(identifier)` - Valida un identificador según las reglas permitidas.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `core.query_builder`, `core.query_utils`, `core.query_validators`.
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno.

El flujo de datos es simple: el archivo recibe payloads y estados visuales, los procesa y devuelve consultas SQL o valores de métricas según sea necesario.

