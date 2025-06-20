from src.config import settings
from src.storage import InMemoryStorage
from src.crawler import SleeperCrawler

def main():
    seed_username = settings.seed_sleeper_username
    storage = InMemoryStorage()
    crawler = SleeperCrawler(seed_username, storage)
    
    # Choose manual or auto mode
    crawler.run(mode="auto", interval=.125)

if __name__ == "__main__":
    main()

