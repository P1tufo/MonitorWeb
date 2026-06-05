# Documentación Técnica - Directorio: core/seed_data
Compilado el: 2026-06-04 23:43:39
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./core/seed_data/widgets.json

### Resumen Funcional
El archivo `widgets.json` contiene una lista de consultas y configuraciones para visualizaciones en un sistema de monitoreo de almacén (WMS). Cada consulta define cómo se deben obtener datos de la base de datos y cómo se deben presentar gráficamente.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements`
  - `outbound_deliveries`
  - `warehouse_tasks`
- **COLUMNAS**:
  - `material`
  - `entrega`
  - `dias_retraso`
  - `fecha_carga`
  - `tipo_operacion`
  - `area_negocio`
  - `warehouse_tasks.material`
  - `warehouse_tasks.entrega`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: Ninguna
- **Archivos que importan a este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno


---

