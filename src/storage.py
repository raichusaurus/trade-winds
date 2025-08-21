from typing import Set
from src.models import SleeperUser, SleeperLeague

class InMemoryStorage:
    def __init__(self):
        self.known_users: Set[SleeperUser] = set()
        self.known_leagues: Set[SleeperLeague] = set()

    def add_user(self, user: SleeperUser) -> bool:
        if user in self.known_users:
            return False
        self.known_users.add(user)
        return True

    def add_league(self, league: SleeperLeague) -> bool:
        if league in self.known_leagues:
            return False
        self.known_leagues.add(league)
        return True
