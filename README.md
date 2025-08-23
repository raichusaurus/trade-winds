# Trade Winds

**Trade Winds** is a modular fantasy football crawler and data engine designed to explore the Sleeper API, analyze trades, and eventually provide player valuation metrics across leagues. The system is built in Python and structured to scale with separate services, a pluggable storage layer, and an upcoming API and persistence layer.

---

## Project Structure

```plaintext
trade_winds/
├── src/
│   ├── crawler_service/          # Core crawler logic and orchestration
│   ├── api_service/              # FastAPI service for health & crawl control (🔜 planned)
│   ├── integrations/             # External API wrappers (e.g., Sleeper)
│   ├── services/                 # Business logic and transformation
│   ├── models/                   # Pydantic data models
│   ├── storage/                  # In-memory & pluggable backend abstraction
│   ├── db/                       # SQLAlchemy models, session, and crud (🔜 planned)
│   ├── utils/                    # Shared helpers (e.g., HTTP with retry logic)
│   └── config/                   # App settings, loaded via environment
│
├── scripts/                      # Helper scripts to run services locally (🔜 planned)
├── tests/                        # Pytest-based test coverage (🔜 planned)
├── requirements.txt              # Python dependencies
├── .env                          # Local environment variable definitions
├── Makefile                      # CLI task shortcuts (🔜 planned)
├── docker-compose.yml            # Local orchestration (🔜 planned)
└── README.md
```

---

## Getting Started

### 1. Clone the repository

bash
git clone https://github.com/raichusaurus/trade-winds.git
cd trade-winds


### 2. Install dependencies

bash
pip install -r requirements.txt


### 3. Add a `.env` file

Create a `.env` file in the root with:

env
SLEEPER_USER_AGENT="TradeWindsDefinitelyNotABot/0.1"

Additional config options (e.g., database URL) will be added as the system evolves.

### 4. Run the crawler manually

From the project root:

bash
python -m src.crawler_service.main --mode auto

Supports `--mode manual` for step-by-step debug-friendly traversal.

---

## Project Goals

* **Traverse Sleeper’s user-league graph** starting from a seed user
* **Track trades** across leagues (with recency filters)
* **Model trade value decay** and player worth based on real user behavior
* **Provide API access** to league metadata and player valuations (🔜)
* **Modular, testable architecture** with swappable components

---

## Roadmap (Epics)

| Epic              | Description                                |
| ----------------- | ------------------------------------------ |
| Project Setup     | Folder structure, config loading, tooling  |
| Crawler (Graph)   | Crawl users and leagues from Sleeper       |
| Crawler (Trades)  | Daily sync of trades since last run (🔜)   |
| Persistence Layer | Postgres + SQLAlchemy + Alembic (🔜)       |
| Admin API         | FastAPI status and control endpoints (🔜)  |
| Dockerization     | Dockerfiles for crawler/API + compose (🔜) |
| Testing & CI      | Pytest, coverage, and GitHub Actions (🔜)  |

---

## Contributing

This repo uses a simplified but organized workflow:

1. Create an issue and link it to an epic (if applicable)
2. Create a branch like `refactor/move-safe-get` or `feat/trade-sync`
3. Make your changes
4. Open a PR and link the issue (`Closes #X`)
5. Merge after review or solo sanity check

Labels like `epic`, `crawler`, `api`, `infra`, and `feature` are used to track work.

---

## 📬 Contact & License

MIT license coming soon. For questions or collaboration ideas, open an issue or [message @raichusaurus on GitHub](https://github.com/raichusaurus).

---
