# Documentación del Proyecto

## Descripción General

Este proyecto contiene el backend para una aplicación destinada a gestionar las faltas de material en la sección de acabados de la División 3 de CAF (Construcciones y Auxiliar de Ferrocarriles). El sistema permite registrar, actualizar, y consultar las faltas de diferentes artículos de los kits que se montan en los bogies

## Estructura del Proyecto

La aplicación está estructurada de la siguiente manera:

-   `alembic/`: Contiene archivos para la migración de la base de datos.
-   `app/`: Directorio principal de la aplicación, donde se encuentran los módulos y subdirectorios para la API, CRUD, modelos, esquemas, servicios, y más.
-   `app/api/`: Contiene los routers de la API para las diferentes entidades del sistema.
-   `app/core/`: Almacena configuraciones y ajustes centrales de la aplicación.
-   `app/crud/`: Contiene las operaciones CRUD para interactuar con la base de datos.
-   `app/db/`: Encargado de la gestión de la base de datos, incluyendo la sesión y los modelos.
-   `app/middlewares/`: Middlewares para el manejo de errores y otras funcionalidades a nivel de aplicación.
-   `app/models/`: Modelos de la base de datos.
-   `app/schemas/`: Esquemas para la validación de datos.
-   `app/services/`: Servicios y lógica de negocio de la aplicación.
-   `tests/`: Directorio para los tests de la aplicación.

## Instalación y Ejecución

### Pre-requisitos

Asegúrate de tener Python y pip instalados en tu sistema. Además, necesitarás tener un entorno virtual configurado y activado.

```bash
pip install -r requirements.txt
```
### Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias para la aplicación, como la cadena de conexión a la base de datos, secretos, y demás configuraciones específicas.

### Ejecución del Servidor en Modo Desarrollo

```bash
uvicorn app.main:app --reload --port 5000 --host 0.0.0.0
```
Este comando inicia la aplicación con `uvicorn`, un servidor ASGI para aplicaciones Python. El flag `--reload` permite recargar automáticamente el servidor cuando se detectan cambios en el código, lo que es útil durante el desarrollo.

## Acceso a la Documentación de la API con Swagger

Una vez el servidor esté en ejecución, podrás acceder a la documentación interactiva de la API proporcionada por Swagger. Para ello, abre tu navegador web y visita la siguiente dirección:

```bash
http://localhost:8000/docs
```
En esta página podrás ver todos los endpoints disponibles, probarlos directamente desde el navegador, y ver los diferentes modelos de datos utilizados en la aplicación.