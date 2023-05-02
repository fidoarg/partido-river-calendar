import pytz

import requests
import locale

from datetime import datetime, date
from bs4 import BeautifulSoup

from textwrap import dedent

COMPETITIONS = {
    "primera-division-de-argentina": {"name":"Liga Profesional de Argentina", "id":"arg.1"},
    "nacional-b": {"name":"Primera Nacional de Argentina", "id":"arg.2"},
    "primera-b-ar": {"name":"Primera B de Argentina", "id":"arg.3"},
    "primera-c-ar": {"name":"Primera C de Argentina", "id":"arg.4"},
    "primera-d-ar": {"name":"Primera D de Argentina", "id":"arg.5"},
    # "copa-arg": {"name":"Copa Argentina", "id":"arg.copa"},
    # "copa-libertadores": {"name":"CONMEBOL Libertadores", "id":"conmebol.libertadores"}
}

def get_data_to_scrap_url(date_to_retreive : date, competition_key : str) -> str:
    """
    Función que recibe la fecha y competición de la cual se quiere obtener información de ESPN
    y devuelve la url donde está la información de los partidos para esa fecha y esa competición

    Parameters
    ----------
        date_to_retreive : date
            datetime.date object of games in case there are any
        competition : str
            Competition which you the agenda for the date_to_retreive is required
    
    Returns
    -------
        url : str
            url to retreive data using a GET request.
    """

    try: 

        competition_id= COMPETITIONS[competition_key]['id']

        url_template = "https://www.espn.com.ar/futbol/fixtures/_/fecha/{year}{month:02d}{day:02d}/liga/{competition_id}"

        url = url_template.format(
            year= date_to_retreive.year,
            month= date_to_retreive.month,
            day= date_to_retreive.day,
            competition_id= competition_id
        )

        return url
    
    except KeyError:
        raise KeyError(f"{competition_key} not found between available competitions")

def get_date_from_table_title(table_title : str) -> date:
    """
    Funcion que recibe el título de la tabla y extrae la fecha del título

    Parameters
    ----------
        table_title : str
            Matches table title which references to a date
    
    Returns
    -------
        table_date : date
            Date referenced by the title
    """
    
    _, str_date, year = [
        element.title().strip()
        for element
        in table_title.split(sep=',')
    ]
    full_str_date = f"{str_date} {year}"
    table_date = datetime.strptime(full_str_date, "%d De %B %Y").date()

    return table_date

def get_venue_datetime_tz(table_title: str, hour_xm_format: str, tz_name: str = "America/Buenos_Aires"):

    time_str, xm = hour_xm_format.split(' ', maxsplit= 1)
    hour, minute = (int(value) for value in time_str.split(':', maxsplit= 1))
    hour = hour + 13 if xm.lower() == 'pm' else hour
    venue_date = get_date_from_table_title(table_title= table_title)
    
    tz = pytz.timezone(tz_name)

    venue_datetime = datetime(
        year= venue_date.year,
        month= venue_date.month,
        day= venue_date.month,
        hour= hour,
        minute= minute
    )
    venue_datetime = tz.localize(venue_datetime)
    return venue_datetime

def structure_row_into_dict(row: BeautifulSoup, table_title:str) -> dict:
    """
    Función que recibe la fila de la tabla de ESPN con la información del partido
    y la estructura en un diccionario según la estructura deseada.

    Parameters
    ----------
        row : BeautifulSoup
            Object with data about the game in an unstructured way.
        table_title : str
            Table title to retreive date from
    
    Returns
    -------
        football_game_info : dict
            Structured dict with game infomation.
    """

    home, away = [element.text for element in row.find_all('span', attrs= {'class': 'Table__Team'})]
    venue = row.find('td', attrs= {'class': 'venue__col'}).text
    hour_str= row.find('td', attrs= {'class': 'date__col'}).text
    datetime_tz= get_venue_datetime_tz(table_title= table_title, hour_xm_format= hour_str)

    football_game_info = dict(
        home_team= home,
        away_team= away,
        venue= venue,
        datetime_tz=datetime_tz.strftime("%Y-%m-%dT%H:%M:%S%z")
    )

    return football_game_info

def get_games_scheduled_in_date(date_to_ckeck : date, competition_key : str) -> list: 
    """
    Función que recibe fecha y competencia y devuelve una lista de partidos
    que se juegan ese día por esa competencia.

    Parameters
    ----------
        date_to_check : date
            Date to check daily games
        competition_key : str
            Competition key to get games

    Returns
    -------
        games : list
            List of diccionaries with game's information
    """
    locale.setlocale(locale.LC_ALL, ('es_ES'))
    
    url = get_data_to_scrap_url(date_to_ckeck, competition_key=competition_key)
    response = requests\
        .get(url=url)\
        .text\
        .encode('utf-8')
    
    responsive_table = BeautifulSoup(response, 'html.parser')\
        .find('div', attrs= {'class': 'ResponsiveTable'})
    table_title = responsive_table\
        .find('div', attrs= {'class': 'Table__Title'})\
        .text\
        .strip()
    table_rows = responsive_table\
        .find('tbody')\
        .find_all('tr')
    
    games_date = get_date_from_table_title(table_title= table_title)
    games = list()
    if games_date == date_to_ckeck:
        for row in table_rows:
            game_info = structure_row_into_dict(row, table_title= table_title)
            game_info['competition_name'] = COMPETITIONS[competition_key]['name']
            games.append(game_info)
    else:
        print(dedent("""
            INFO
            ----
            No games in date
        """))

    return games