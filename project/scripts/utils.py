import requests
import os

from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime

from google_calendar import build_calendar_event


def get_next_matches_from_date() -> dict:
    print(os.getcwd())
    response = requests.get(
        "https://www.cariverplate.com.ar/calendario-de-partidos"
    ).text.encode("utf-8")

    soup = BeautifulSoup(response, "html.parser")
    elements = soup.find_all(class_="d_calendario")

    for element in elements[:2]:
        print(build_calendar_event(parse_match_element(element=element)))


def get_match_datetime(text: str) -> datetime:
    """
    Function that receives part of the web scapped text and defines the date and time 
    for the game.

    Parameters
    ----------
        text : str
            Web scrapped text that contains the information of the time and date of the game.

    Returns
    -------
        game_datetime : datetime
            Text converted into datetime object.

    """

    weekday_dt, time = text.lower()[3:].split(" - ")
    dt_str = weekday_dt.split(" ")[-1]

    time_splitted = [int(value) for value in time.split(".")]
    hour, minutes = time_splitted[0], time_splitted[1] if len(time_splitted) > 1 else 0

    game_datetime = datetime.strptime(f"{dt_str} {hour}:{minutes}", "%d/%m/%Y %H:%M")
    game_datetime = timezone("America/Buenos_Aires").localize(game_datetime)

    return game_datetime


def home_or_away(match_title: str) -> str:
    """
    Receives the match title as a string and difines if it is an 'away' or 'home'
    game for River Plate.

    Parameters
    ----------
        match_title : str
            Match title which tells which teams are playing.
    
    Returns
    -------
        output : str ('home' or 'away')
            Defines if it is a home or away game based on it's title.
    """
    teams = [value.strip().lower() for value in match_title.split("Vs.")]
    return "home" if teams[0] == "river plate" else "away"


def parse_match_element(element):
    match_title = element.find(class_="text-uppercase").text.title()
    competition = element.find("p").find("strong").text
    match_datetime_str = "".join(
        element.find("p").findAll(string=True, recursive=False)
    ).strip()
    match_datetime = get_match_datetime(match_datetime_str)

    return {
        "match_title": match_title,
        "competition": competition,
        "datetime": match_datetime,
        "stadium": home_or_away(match_title),
    }


if __name__ == "__main__":
    get_next_matches_from_date()
