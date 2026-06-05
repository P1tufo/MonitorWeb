## Archivo: ./tests/test_auth.py

### Resumen Funcional
Este archivo contiene pruebas unitarias para el módulo de autenticación JWT en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de inicio de sesión, registro de usuarios y gestión de perfiles de usuario.

### Catálogo de Funciones y Clases
- `test_login_page_renders(client)` - Verifica que la página de login sea accesible.
- `test_login_success(client)` - Verifica login exitoso con credenciales del admin por defecto.
- `test_login_wrong_password(client)` - Verifica que credenciales incorrectas retornen 401.
- `test_me_endpoint_without_token(client)` - Verifica que /me sin token retorne 401.
- `test_me_endpoint_with_token(client)` - Verifica que /me con token válido retorne el perfil del usuario.
- `test_register_requires_admin(client)` - Verifica que registrar un usuario requiera token de admin.
- `test_register_and_login_new_user(client)` - Verifica el flujo completo: admin registra usuario → nuevo usuario hace login.
- `test_list_users_admin_only(client)` - Verifica que listar usuarios requiera rol admin.

### Interacción con Base de Datos
Ninguna. Las pruebas se realizan utilizando un cliente de prueba (`TestClient`) proporcionado por FastAPI, sin acceso directo a una base de datos.

### Estado y Variables Globales
Ninguna. Todas las variables utilizadas son locales dentro de las funciones de prueba.

### Dependencias y Flujo
- **Dependencias**: `pytest`, `fastapi.testclient.TestClient`.
- **Flujo de Datos**:
  - El archivo importa `pytest` y `TestClient` desde `fastapi.testclient`.
  - No hay archivos del proyecto que importen a este archivo.
  - Las pruebas realizan solicitudes HTTP al servidor FastAPI utilizando el cliente de prueba, lo que implica un flujo de datos entre el cliente y el servidor.

