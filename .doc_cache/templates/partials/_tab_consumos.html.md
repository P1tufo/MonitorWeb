## Archivo: ./templates/partials/_tab_consumos.html

### Resumen Funcional
Este fragmento HTML corresponde a una pestaña dentro de un sistema de monitoreo de almacén (WMS) que permite analizar los consumos y costos de materiales. Permite buscar por Centro de Costo o por materiales específicos, mostrando históricos mensuales y anuales.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla `movimientos` (Mov. 201): 
    - `id`
    - `material_id`
    - `centro_costo_id`
    - `cantidad`
    - `precio_unitario`
    - `fecha`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno
- **Flujo de Datos:** El archivo se utiliza para renderizar la interfaz de usuario y no interactúa directamente con el backend o base de datos.

