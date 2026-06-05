## Archivo: ./static/js/consumos.js

### Resumen Funcional
Este archivo JavaScript (`consumos.js`) es parte del sistema de monitoreo de almacén (WMS). Se encarga de manejar la interacción con el usuario, como buscar materiales por Centro de Costo (CeCo) o por lista de materiales ingresada en un textarea. También se encarga de renderizar tablas y mostrar tendencias mensuales de los materiales.

### Catálogo de Funciones y Clases
- `handlePaste(e)` - Obsoleto: Manejaba el pegado de múltiples líneas, pero ahora es obsoleto.
- `limpiarGrilla()` - Limpia la grilla y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero.
- `formatearNumero(valor)` - Formatea un valor numérico como número.
- `filterTable(tableId)` - Filtra una tabla según los valores ingresados en las celdas de filtro.
- `renderVanillaTable(tbodyId, data, columns, onRowClick = null)` - Renderiza una tabla usando JavaScript puro.
- `buscarPorCeCo()` - Busca materiales por Centro de Costo y muestra los resultados.
- `buscarPorMateriales()` - Busca materiales ingresados en un textarea y muestra los resultados.
- `abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '')` - Abre el modal con la tendencia mensual del material.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencia.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las consultas y operaciones se realizan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena el estado del gráfico de tendencias mensuales.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**:
  - `consumos.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no se especifican los detalles específicos en este fragmento.

