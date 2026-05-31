## Archivo: ./static/js/consumos.js

### Resumen Funcional
El archivo `consumos.js` contiene funciones y métodos para gestionar la interfaz de usuario y el procesamiento de datos relacionados con los consumos en materiales. Permite buscar y filtrar datos por Centro de Costo (CeCo) o por materiales, muestra resultados en una tabla y permite visualizar tendencias mensuales de consumo.

### Catálogo de Funciones y Clases
- `handlePaste(e)` - Maneja el evento de pegado para rellenar múltiples celdas.
- `limpiarGrilla()` - Limpia la grilla de entrada y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero.
- `formatearNumero(valor)` - Formatea un valor numérico como número.
- `filterTable(tableId)` - Filtra una tabla según los valores en las celdas de entrada de la cabecera.
- `renderVanillaTable(tbodyId, data, columns, onRowClick = null)` - Renderiza una tabla usando elementos HTML y JavaScript puro.
- `buscarPorCeCo()` - Busca datos por Centro de Costo y muestra los resultados en una tabla.
- `buscarPorMateriales()` - Busca datos por materiales ingresados en la grilla y muestra los resultados en una tabla.
- `abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '')` - Abre un modal con la tendencia mensual de consumo para un material específico.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencia.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena una instancia del gráfico de tendencias mensuales.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para renderizar el gráfico de tendencias).
- **Flujo Interno**: El archivo interactúa con elementos HTML para mostrar resultados, manejar eventos de usuario y realizar peticiones a una API para obtener datos.

