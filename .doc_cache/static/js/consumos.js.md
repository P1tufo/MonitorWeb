## Archivo: ./static/js/consumos.js

### Resumen Funcional
El archivo `consumos.js` es un script JavaScript que se ejecuta en el navegador y proporciona funcionalidades para interactuar con una interfaz de usuario web, permitiendo la entrada de datos en una grilla similar a Excel, filtrado de tablas y búsqueda de consumos por Centro de Costo (CeCo) o materiales.

### Catálogo de Funciones y Clases
- `document.addEventListener('DOMContentLoaded', callback)` - Inicializa el script cuando el DOM esté completamente cargado.
- `handlePaste(e)` - Maneja el evento de pegar en las celdas de la grilla, permitiendo la entrada de múltiples valores a la vez.
- `limpiarGrilla()` - Limpia los valores de todas las celdas y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero con símbolo y formato localizado.
- `formatearNumero(valor)` - Formatea un valor numérico con formato localizado.
- `filterTable(tableId)` - Filtra las filas de una tabla según los valores ingresados en las celdas de filtro.
- `renderVanillaTable(tbodyId, data, columns)` - Renderiza datos en una tabla HTML utilizando JavaScript puro.
- `buscarPorCeCo()` - Busca y muestra los consumos asociados a un Centro de Costo específico.
- `buscarPorMateriales()` - Busca y muestra los consumos asociados a materiales ingresados en la grilla.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales ni se utiliza estado crítico almacenado en variables.

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El script interactúa con elementos del DOM para crear una grilla de entrada, manejar eventos de pegar, filtrar tablas y realizar búsquedas. Los resultados de las búsquedas son renderizados en tablas HTML utilizando funciones JavaScript puro.

