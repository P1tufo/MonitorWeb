## Archivo: ./test_deliveries.py

### Resumen Funcional
El archivo `test_deliveries.py` es un script de prueba que interactúa con una base de datos para obtener y mostrar el contexto completo de entregas.

### Catálogo de Funciones y Clases
- `svc.get_full_context()` - Obtiene el contexto completo de entregas.

### Interacción con Base de Datos
- **Motor:** No especificado.
- **Tablas:** No aplica.
- **Columnas:** No aplica.
- **Consultas SQL Crudas/ORM:** Sí, utiliza `DeliveriesService` que probablemente realiza consultas a la base de datos.

### Estado y Variables Globales
- `db` - Variable global que almacena una instancia de la sesión de la base de datos.

### Dependencias y Flujo
- **Librerías Externas:** `sys`, `logging`.
- **Flujo Interno:** El script crea una instancia de `DeliveriesService`, obtiene el contexto completo de entregas, e imprime las claves del contexto. Si ocurre un error, se imprime la traza de excepción.

### Notas Adicionales
El archivo no realiza ninguna interacción directa con tablas o columnas específicas en la base de datos; en su lugar, utiliza un servicio para obtener el contexto completo de entregas.

