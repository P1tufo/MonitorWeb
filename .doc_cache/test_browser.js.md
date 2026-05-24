## Archivo: ./test_browser.js

### Resumen Funcional
El archivo `test_browser.js` es un script que automatiza el lanzamiento de un servidor Python en segundo plano y luego utiliza Playwright para abrir un navegador Chromium, navegar a una página web local, desmarcar un checkbox y cerrar el navegador.

### Catálogo de Funciones y Clases
- `main()` - Función principal que coordina la ejecución del script.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- `playwright` - Librería utilizada para controlar el navegador Chromium.
- `child_process` - Módulo Node.js utilizado para ejecutar comandos del sistema operativo (lanzar el servidor Python).
- El script se comunica con otros archivos del proyecto a través de la ejecución del comando `python3 main.py`, lo que implica que debe haber un archivo `main.py` en el mismo directorio o en una ruta relativa.

