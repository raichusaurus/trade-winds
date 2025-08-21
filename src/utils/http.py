import requests
from time import sleep
import random

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
