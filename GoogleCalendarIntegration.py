import os.path
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarManager:
    def __init__(self):
        # Inicializa el servicio al autenticarse
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        # Verifica si ya existe un archivo de token
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # Si no hay credenciales válidas, realiza la autenticación
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Autenticación interactiva si no hay credenciales o están vencidas
                flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
                creds = flow.run_local_server(port=0)

            # Guarda las credenciales para la siguiente ejecución
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    def list_upcoming_events(self, max_results=10):
        # Obtén la fecha y hora actuales en formato UTC
        now = dt.datetime.utcnow().isoformat() + "Z"
        # Calcula la fecha y hora de mañana a esta misma hora
        tomorrow = (dt.datetime.now() + dt.timedelta(days=5)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + "Z"

        # Obtiene los eventos próximos en el rango de fechas
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, timeMax=tomorrow,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Muestra los eventos próximos o un mensaje si no hay eventos
        if not events:
            print('No se encontraron eventos próximos.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'], event['id'])

        return events

    def create_event(self, summary, start_time, end_time, timezone, attendees=None):
        # Crea un nuevo evento con la información proporcionada
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        }

        # Agrega asistentes si se proporcionan
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            # Inserta el evento en el calendario y muestra el enlace al evento creado
            event = self.service.events().insert(calendarId="primary", body=event).execute()
            print(f"Evento creado: {event.get('htmlLink')}")
        except HttpError as error:
            print(f"Ha ocurrido un error: {error}")

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        # Obtiene el evento existente por su ID
        event = self.calendar_service.events().get(calendarId='primary', eventId=event_id).execute()

        # Actualiza la información del evento si se proporciona
        if summary:
            event['summary'] = summary

        if start_time:
            event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')

        if end_time:
            event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Actualiza el evento en el calendario y devuelve el evento actualizado
        updated_event = self.calendar_service.events().update(
            calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event

    def delete_event(self, event_id):
        # Elimina el evento del calendario por su ID
        self.calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True

# Crea una instancia de GoogleCalendarManager
calendar = GoogleCalendarManager()

# Lista los próximos eventos
calendar.list_upcoming_events()

# Crea un nuevo evento de ejemplo
calendar.create_event("Reunion QA", "2024-02-16T16:30:00-05:00", "2024-02-16T17:30:00-05:00", "America/Lima", ["gp@gmail.com", "fles@lex.pe"])
