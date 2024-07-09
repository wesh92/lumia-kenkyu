import tomllib
import enum

with open('.secrets.toml', "rb") as f:
    API_KEY = tomllib.load(f)['er_api']['key']


BASE_URL = 'https://open-api.bser.io/'
CURRENT_SEASON = 25 # Season 4 "SUNSET"
HEADERS = {
    'Accept': 'application/json',
    "x-api-key": API_KEY
}

class version(enum.Enum):
    v1 = 'v1'
    v2 = 'v2'

class endpoints(enum.Enum):
    game = {
        "fetch_by_id": 'games/{game_id}',
    }
    rank = {
    "seasonal_top_rankers": 'rank/top/{season_id}/{mode_id}',
    "user_rank": 'rank/user/{user_id}/{season_id}/{mode_id}',
    }
    user = {
        "fetch_user_games": 'user/games/{user_id}',
        "info_by_username": 'user/nickname/',
        "user_season_stats": 'user/stats/{userNum}/{seasonId}',
    }
