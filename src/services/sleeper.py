from typing import List, Tuple
from pydantic import ValidationError

from src.integrations import sleeper
from src.models.sleeper import SleeperUser, SleeperLeague, SleeperRoster

def fetch_user_id(username: str) -> str:
    user_data = sleeper.get_user(username)
    try:
        user = SleeperUser(**user_data)
        return user.user_id
    except ValidationError as e:
        print(f"Validation error parsing user data: {e}")
        raise

def fetch_user_leagues(user_id: str, season: str = "2025") -> List[SleeperLeague]:
    leagues_data = sleeper.get_user_leagues(user_id, season)
    try:
        return [SleeperLeague(**league) for league in leagues_data]
    except ValidationError as e:
        print(f"Validation error parsing league data: {e}")
        raise

def fetch_league_users_and_rosters(league_id: str) -> Tuple[List[SleeperUser], List[SleeperRoster]]:
    users_data = sleeper.get_league_users(league_id)
    users = []
    rosters = []

    for user_json in users_data:
        try:
            user = SleeperUser(**user_json)
            users.append(user)

            roster = SleeperRoster(
                league_id=league_id,
                user_id=user.user_id,
                team_name=user_json.get("metadata", {}).get("team_name")
            )
            rosters.append(roster)
        except ValidationError as e:
            print(f"Validation error parsing user/roster data: {e}")
            continue

    return users, rosters
