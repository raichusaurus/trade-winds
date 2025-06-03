import requests
from time import sleep
import random
from typing import List
from pydantic import ValidationError
from src.models import SleeperUser, SleeperLeague

MAX_RETRIES = 3
BASE_DELAY = 1  # in seconds
MAX_DELAY = 10  # max delay between retries
HEADERS = {
    "User-Agent": "TradeWindsDefinitelyNotABot/0.1 (Sleeper: @raichusaurus)"
}

def safe_get(url: str) -> dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            print(f"⚠️ Server error ({e.response.status_code}), retrying... [{attempt}/{MAX_RETRIES}]")
        except requests.RequestException as e:
            print(f"⚠️ Request failed ({e}), retrying... [{attempt}/{MAX_RETRIES}]")

        # Exponential backoff with jitter
        delay = min(BASE_DELAY * (2 ** (attempt - 1)), MAX_DELAY)
        delay = delay * random.uniform(0.8, 1.2)  # add jitter
        sleep(delay)

    raise RuntimeError(f"❌ Failed to fetch data after {MAX_RETRIES} attempts: {url}")

def get_user(username: str) -> str:
    url = f"https://api.sleeper.app/v1/user/{username}"
    return safe_get(url)

def get_user_leagues(user_id: str, season: str = "2025") -> List[SleeperLeague]:
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{season}"
    return safe_get(url)

def get_league_users(league_id: str) -> List[SleeperUser]:
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    return safe_get(url)