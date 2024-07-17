import tomllib
import enum
import os

with open(".secrets.toml", "rb") as f:
    secrets = tomllib.load(f)
    API_KEY = secrets["er_api"]["key"]
    SUPABASE_URL = secrets["supabase"]["url"]
    SUPABASE_KEY = secrets["supabase"]["key"]

MATCHES_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples"
ARCHIVE_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples/archive"
ERROR_PATH = os.path.join(os.path.dirname(ARCHIVE_PATH), "error")

BASE_URL = "https://open-api.bser.io/"
CURRENT_SEASON = 25  # Season 4 "SUNSET"
HEADERS = {"Accept": "application/json", "x-api-key": API_KEY}


class version(enum.Enum):
    v1 = "v1"
    v2 = "v2"


class endpoints(enum.Enum):
    game = {
        "fetch_by_id": "games/{game_id}",
    }
    rank = {
        "seasonal_top_rankers": "rank/top/{season_id}/{mode_id}",
        "user_rank": "rank/user/{user_id}/{season_id}/{mode_id}",
    }
    user = {
        "fetch_user_games": "user/games/{user_id}",
        "fetch_by_username": "user/nickname/",
        "user_season_stats": "user/stats/{userNum}/{seasonId}",
    }
