from typing import List
from pydantic import ValidationError
from src.models import SleeperUser, SleeperLeague
from src.utils.http import safe_get

def get_user(username: str) -> str:
    url = f"https://api.sleeper.app/v1/user/{username}"
    return safe_get(url)

def get_user_leagues(user_id: str, season: str = "2025") -> List[SleeperLeague]:
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{season}"
    return safe_get(url)

def get_league_users(league_id: str) -> List[SleeperUser]:
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    return safe_get(url)