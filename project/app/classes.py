from dataclasses import dataclass

@dataclass
class Game:
    home_team: str
    away_team: str
    venue: str
    competition_name: str
    datetime_tz: str