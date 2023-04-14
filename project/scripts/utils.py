import requests

from bs4        import BeautifulSoup
from datetime   import datetime

def get_next_matches_from_date() -> dict:

    response =requests.get("https://www.cariverplate.com.ar/calendario-de-partidos").text.encode('utf-8')
 
    soup = BeautifulSoup(response, "html.parser")
    elements = soup.find_all(class_='d_calendario')
    
    for element in elements:
        
        print(parse_match_element(element= element))

def get_match_datetime(text : str):
    weekday_dt, time = text.lower()[3:].split(' - ')
    dt_str = weekday_dt.split(' ')[-1]

    time_splitted = [int(value) for value in time.split('.')]
    hour, minutes = time_splitted[0], time_splitted[1] if len(time_splitted) > 1 else 0

    dt = datetime.strptime(f"{dt_str} {hour}:{minutes}", '%d/%m/%Y %H:%M')
    
    return dt


def parse_match_element(element):
    match_title= element.find(class_='text-uppercase').text
    competition= element.find('p').find('strong').text
    match_datetime_str= ''.join(element.find('p').findAll(text=True, recursive=False)).strip()
    dt = get_match_datetime(match_datetime_str)

    return {
        "match_title": match_title,
        "competition": competition, 
        "datetime": dt
    }

if __name__ == "__main__":
    get_next_matches_from_date(None)
