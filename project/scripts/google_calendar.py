from datetime import timedelta, datetime


def build_calendar_event(match_data: dict, match_duration_hrs: int = 2) -> dict:
    """
    Función que recibe un diccionario con la información del partido
    y construye el evento con la estructura para la API de Google Calendar

    Parameters
    ----------
        match_data : dict
            Objeto clave valor con información sobre el partido
        match_duration_hrs : int (default = 2)
            Duración del partido en horas.

    Returns
    -------
        calendar_event : dict
            Objeto clave valor con la estructura necesaria para construir
            un evento a través de la API de Google Calendar con sus valores
            completados.
    """
    match_start = match_data.get("match_dt")
    match_end = (
            datetime.strptime(match_data.get("match_dt"), "%Y-%m-%dT%H:%M:%S%z")
        +   timedelta(hours=2)
        ).strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )
    calendar_event = {
        "summary": match_data.get("match_title"),
        "description": match_data.get("competition"),
        "start": {
            "dateTime": match_start,
            "timeZone": f"America/Buenos_Aires",
        },
        "end": {
            "dateTime": match_end,
            "timeZone": "America/Buenos_Aires",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    return calendar_event
