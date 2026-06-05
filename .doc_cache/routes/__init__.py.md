## Archivo: ./routes/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para las rutas del sistema de monitoreo de almacén (WMS). Importa y registra todas las subrutas relacionadas con diferentes funcionalidades como el panel de control, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización y configuraciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: FastAPI.
- **Archivos del Proyecto que IMPORTAN a este archivo**:
  - `dashboard`
  - `deliveries`
  - `inventory`
  - `analytics_proyecciones`
  - `filters`
  - `pdf`
  - `sync`
  - `docs`
  - `settings`

Este archivo no importa ninguna clase o función específica, solo registra las subrutas. El flujo de datos se maneja a través de FastAPI para la definición y gestión de rutas.

