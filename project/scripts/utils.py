import requests

from datetime import datetime
from typing import Tuple

from bs4 import BeautifulSoup
from pytz import timezone

from google_calendar import build_calendar_event


def get_next_matches_from_date() -> dict:
    response = requests.get(
        "https://www.cariverplate.com.ar/calendario-de-partidos"
    ).text.encode("utf-8")

    soup = BeautifulSoup(response, "html.parser")
    elements = soup.find_all(class_="d_calendario")

    for element in elements:
        print(parse_match_element(element=element))


def get_match_datetime(text: str) -> datetime:
    """
    Función que recibe texto desestructurado de la fecha y hora del
    partido y devuelve un objeto datetime con timezone de America/Buenos_Aires

    Parameters
    ----------
        text : str
            Unstructured text with match datetime information

    Returns
    -------
        match_datetime : datetime
            Timezoned datetime object with date and time with 'America/Buenos_Aires' timezone.
    """

    weekday_dt, time = text.lower()[3:].split(" - ")
    dt_str = weekday_dt.split(" ")[-1]

    time_splitted = [int(value) for value in time.split(".")]
    hour, minutes = time_splitted[0], time_splitted[1] if len(time_splitted) > 1 else 0

    match_datetime = datetime.strptime(f"{dt_str} {hour}:{minutes}", "%d/%m/%Y %H:%M")
    match_datetime = timezone("America/Buenos_Aires").localize(match_datetime)

    return match_datetime


def get_rival_and_condition(match_title: str) -> Tuple[str, str]:
    """
    Función que extrae del título del partido el rival y la condición.

    Parameters
    ----------
        match_title : str
            Match title that provides information about the rival and the condition

    Returns
    -------
        rival : str
            Rival to play against
        condition : str ('home', 'away)
            Condition in which River plays.
    """

    match_title = match_title.lower()
    teams = [value.strip() for value in match_title.split("vs.")]
    rival, condition = (
        (teams[1].title(), "home")
        if teams[0] == "river plate"
        else (
            teams[0].title(),
            "away",
        )
    )

    return rival, condition


def parse_match_element(element: BeautifulSoup) -> dict:
    """
    Función que recibe el elemento de BeautifulSoup con toda la información de la
    fecha y la estructura en un diccionario.

    Parameters
    ----------
        element : BeautifulSoup
            Element with all the match information required

    Returns
    -------
        match_data : dict
            Python Diccionary with all the match information structured
    """
    match_title = element.find(class_="text-uppercase").text.title()
    competition = element.find("p").find("strong").text
    match_datetime_str = "".join(
        element.find("p").findAll(string=True, recursive=False)
    ).strip()

    match_datetime = get_match_datetime(match_datetime_str)
    rival, condition = get_rival_and_condition(match_title)

    match_data = dict(
        match_title=match_title,
        competition=competition,
        match_dt=match_datetime.strftime("%Y-%m-%dT%H:%M:%S%z"),
        rival=rival,
        condition=condition,
    )

    return match_data


if __name__ == "__main__":
    get_next_matches_from_date()
