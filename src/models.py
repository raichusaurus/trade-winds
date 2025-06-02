from pydantic import BaseModel

class SleeperUser(BaseModel):
    user_id: str
    display_name: str

    def __hash__(self):
        return hash(self.user_id)

    def __eq__(self, other):
        return isinstance(other, SleeperUser) and self.user_id == other.user_id

class SleeperLeague(BaseModel):
    league_id: str
    name: str
    total_rosters: int
    season: str

    def __hash__(self):
        return hash(self.league_id)

    def __eq__(self, other):
        return isinstance(other, SleeperLeague) and self.league_id == other.league_id