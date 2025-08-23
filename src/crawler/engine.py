import time
from src.storage.in_memory import InMemoryStorage
from src.services.sleeper import fetch_user_id, fetch_user_leagues, fetch_league_users_and_rosters

class SleeperCrawler:
    def __init__(self, seed_username: str, storage: InMemoryStorage):
        self.seed_username = seed_username
        self.storage = storage
        self.user_queue = []
        self.league_queue = []

        # Initialize
        seed_user_id = fetch_user_id(seed_username)
        self.user_queue.append(seed_user_id)
        self.storage.known_users.add(seed_user_id)

    def print_state(self):
        print("****Current state:")
        print(f"known users: {len(self.storage.known_users)}")
        print(f"known leagues: {len(self.storage.known_leagues)}")
        print(f"users in queue: {len(self.user_queue)}")
        print(f"leagues in queue: {len(self.league_queue)}")

    def crawl(self):
        while self.user_queue or self.league_queue:
            while self.user_queue:
                user_id = self.user_queue.pop(0)
                leagues = fetch_user_leagues(user_id)
                for league in leagues:
                    if league not in self.storage.known_leagues:
                        self.storage.known_leagues.add(league)
                        self.league_queue.append(league.league_id)
                yield ()                      
            if self.league_queue:
                league_id = self.league_queue.pop(0)
                users, rosters = fetch_league_users_and_rosters(league_id)
                for user in users:
                    if user not in self.storage.known_users:
                        self.storage.known_users.add(user)
                        self.user_queue.append(user.user_id)
                yield ()

    def run(self, mode: str = "auto", interval: float = 1.0):
        if mode == "manual":
            for step in self.crawl():
                self.print_state()
                input("➡️ Press Enter to continue...")
        elif mode == "auto":
            for step in self.crawl():
                self.print_state()
                time.sleep(interval)
        else:
            raise ValueError("Mode must be 'manual' or 'auto'")
