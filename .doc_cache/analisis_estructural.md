## Análisis de Arquitectura Global

### Arquitectura General Detectada

La estructura del proyecto sugiere una arquitectura **Modular**. Esto se debe a la organización de los módulos y carpetas que separan diferentes aspectos del sistema, como el núcleo (`core`), las rutas (`routes`), los repositorios (`repositories`), los servicios (`services`) y las pruebas (`tests`). Además, la presencia de una carpeta `docs` para documentación y una carpeta `scripts` para scripts adicionales también apoya esta arquitectura modular.

### Propósito Probable de las Carpetas Principales

- **core/**: Contiene el código central del sistema, incluyendo configuraciones, utilidades generales, modelos de datos, y lógica de negocio.
- **routes/**: Define las rutas de la aplicación web, mapeando URLs a funciones de controlador.
- **repositories/**: Almacena los repositorios que manejan la interacción con la base de datos y el almacenamiento persistente.
- **services/**: Contiene los servicios que encapsulan la lógica de negocio compleja.
- **tests/**: Incluye las pruebas unitarias y de integración para asegurar que el sistema funcione correctamente.

### Organización Lógica de las Dependencias

La organización de dependencias es coherente con una arquitectura modular:

1. **Dependencias Internas**:
   - `core/` depende de `config.py`, `utils.py`, y otros módulos dentro del mismo directorio.
   - `routes/` depende de los servicios definidos en `services/`.
   - `repositories/` dependen de modelos definidos en `core/models.py`.

2. **Dependencias Externas**:
   - El proyecto utiliza bibliotecas externas como Flask para el framework web, SQLAlchemy para ORM, y otras herramientas de análisis y procesamiento de datos.

3. **Pruebas**:
   - Las pruebas (`tests/`) dependen de los módulos principales del sistema, asegurando que todos los componentes funcionen juntos correctamente.

4. **Documentación**:
   - La carpeta `docs` contiene documentación para diferentes partes del proyecto, lo que facilita el mantenimiento y la comprensión del código.

5. **Recursos Estáticos**:
   - La carpeta `static/` almacena archivos CSS y JavaScript necesarios para la interfaz de usuario.
   - La carpeta `templates/` contiene los archivos HTML de las vistas.

6. **Datos y Archivos Adicionales**:
   - La carpeta `data/` contiene archivos de base de datos y otros recursos adicionales.
   - La carpeta `DELIVERIES_cleansed/` almacena datos limpios para análisis.

Esta estructura modular facilita el mantenimiento, la escalabilidad y la colaboración entre equipos en un proyecto de software.

