from dataclasses import dataclass
from interfaces import Entity, Parser, Scrapper

from scrapping.espn.football.constants import TEAMS_BASE_URL

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@dataclass
class TeamEntity(Entity):

    name: str
    espn_name: str
    espn_id: int

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def exists(self):
        pass

    @property
    def home_url(self):

        return "/".join([TEAMS_BASE_URL, f"_/id/{self.espn_id}/{self.espn_name}"])
    
    @property
    def calendar_url(self):

        return "/".join([TEAMS_BASE_URL, f"calendario/_/id/{self.espn_id}/{self.espn_name}"])
    
    @property
    def results_url(self):

        return "/".join([TEAMS_BASE_URL, f"resultados/_/id/{self.espn_id}/{self.espn_name}"])

class TeamParser(Parser):
    
    def execute(self):
        ...

class TeamScrapper(Scrapper):

    def __init__(self, headless: bool, team: TeamEntity) -> None:

        self.team = team
        self.headless = headless

    def __enter__(self) -> webdriver.Chrome:

        options = Options()
        if self.headless:
            options.add_argument("--headless")

        self.web_driver = webdriver.Chrome(chrome_options= options)
        
        return self
    
    def execute(self):
        ...

        
    def __exit__(self, exc_type, exc_value, traceback):
        print(
            exc_type, exc_value, traceback
        )
        self.web_driver.close()



        

    

