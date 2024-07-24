import tomllib
import enum
import os
from typing import Any

# with open(".secrets.toml", "rb") as f:
#     secrets = tomllib.load(f)
#     API_KEY = secrets["er_api"]["key"]
#     SUPABASE_URL = secrets["supabase"]["url"]
#     SUPABASE_KEY = secrets["supabase"]["key"]


class DAOType(enum.Enum):
    API_ONLY = "api_only"
    SUPABASE = "supabase"
    POSTGRES = "postgres"
    DRAGONFLYDB = "dragonfly"


class Environment(enum.Enum):
    DEV = "dev"
    PROD = "prod"


def get_secrets(
    dao_type: DAOType, environment: Environment = Environment.DEV
) -> dict[str, Any] | NotImplementedError | ValueError | None:
    with open(".secrets.toml", "rb") as f:
        secrets = tomllib.load(f)
        if dao_type == DAOType.API_ONLY:
            return {"api_key": secrets["er_api"]["key"]}
        elif dao_type == DAOType.SUPABASE:
            supabase_secrets = secrets["supabase"][0][environment.value][0]
            return {
                "url": supabase_secrets["url"],
                "key": supabase_secrets["key"],
            }
        elif dao_type == DAOType.DRAGONFLYDB:
            dragonfly_secrets = secrets["dragonfly"][0][environment.value][0]
            return {
                "url": dragonfly_secrets["host"],
                "port": dragonfly_secrets["port"],
                "password": dragonfly_secrets["password"],
                "key_namespace": dragonfly_secrets["namespace"],
            }
        elif dao_type == DAOType.POSTGRES:
            NotImplementedError("Postgres secrets not implemented.")
        else:
            raise ValueError(
                "Invalid DAO or Environement type.\n Your input: dao_type: {dao_type}, environment: {environment}"
            )


MATCHES_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples"
ARCHIVE_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples/archive"
ERROR_PATH = os.path.join(os.path.dirname(ARCHIVE_PATH), "error")

BASE_URL = "https://open-api.bser.io/"
CURRENT_SEASON = 25  # Season 4 "SUNSET"
HEADERS = {
    "Accept": "application/json",
    "x-api-key": get_secrets(DAOType.API_ONLY)["api_key"],
}


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
