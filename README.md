# Google Calendar Manager

Este script en Python permite gestionar eventos en Google Calendar utilizando la API de Google Calendar.

## Requisitos

- Python 3.x
- Bibliotecas externas (instalables mediante `pip install -r requirements.txt`):
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`

## Configuración

1. **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    ```

2. **Instalar Dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Obtener Credenciales de la API de Google Calendar:**

    - Sigue los siguientes pasos para obtener las credenciales:
        1. Accede a [Google Cloud Console](https://console.cloud.google.com/).
        2. Crea un nuevo proyecto o selecciona uno existente.
        3. En el panel de navegación, haz clic en "API y Servicios" > "Biblioteca".
        4. Busca "Google Calendar API" y actívala para tu proyecto.
        5. En el panel de navegación, haz clic en "API y Servicios" > "Credenciales".
        6. Haz clic en "Crear credenciales" y selecciona "ID de cliente de OAuth".
        7. Configura la aplicación como "Otra aplicación de escritorio".
        8. Descarga el archivo JSON de las credenciales y guárdalo como `client_secret.json` en el mismo directorio que el script.

## Uso

1. **Ejecutar el Script:**

    ```bash
    python GoogleCalendarIntegration.py
    ```

2. **Autenticación:**

    - Sigue las instrucciones en la consola para autenticarte con Google.
    - Las credenciales se guardarán en un archivo `token.json` para futuras ejecuciones.

3. **Funcionalidades:**

    - Utiliza las opciones del script para listar eventos próximos, crear nuevos eventos, actualizar eventos existentes y eliminar eventos.

## Ejemplo

```python
# Crear una instancia del gestor de Google Calendar
calendar = GoogleCalendarManager()

# Listar los próximos eventos
calendar.list_upcoming_events()

# Crear un nuevo evento de ejemplo
calendar.create_event("Reunion QA", "2024-02-16T16:30:00-05:00", "2024-02-16T17:30:00-05:00", "America/Lima", ["gp@gmail.com", "fles@lex.pe"])

