import tomllib
import enum
import os


class DBProvider(enum.Enum):
    SUPABASE = "supabase"
    TURSO = "turso"
    API_ONLY = "api_only"


def get_provider_secrets(
    provider: DBProvider = DBProvider.SUPABASE,
) -> dict[str, str] | str:
    """Get the secrets for the specified provider.

    Args:
        provider (DBProvider, optional): The provider to get the secrets for. Defaults to DBProvider.SUPABASE.
            API_ONLY: Only return the API key.
            SUPABASE: Return the API key, URL, and key.
            TURSO: Return the API key, URL, and key.
        See:
            DBProvider: The enum of providers.

    Returns:
        dict[str, str] | str: The secrets for the specified provider.
            If the provider is API_ONLY, return the API key as a string.
            If the provider is SUPABASE, return a dictionary with the API key, URL, and key in that order.
            If the provider is TURSO, return a dictionary with the API key, URL, and key in that order.

    Raises:
        FileNotFoundError: If the .secrets.toml file is not found.
    """
    with open(".secrets.toml", "rb") as f:
        secrets = tomllib.load(f)
        API_KEY = secrets["er_api"]["key"]
        if provider == DBProvider.API_ONLY:
            return API_KEY
        if provider == DBProvider.SUPABASE:
            SUPABASE_URL = secrets["supabase"]["url"]
            SUPABASE_KEY = secrets["supabase"]["key"]
            return {"API_KEY": API_KEY, "URL": SUPABASE_URL, "KEY": SUPABASE_KEY}
        elif provider == DBProvider.TURSO:
            TURSO_URL = secrets["turso"]["url"]
            TURSO_KEY = secrets["turso"]["KEY"]
            return {"API_KEY": API_KEY, "URL": TURSO_URL, "KEY": TURSO_KEY}


MATCHES_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples"
ARCHIVE_PATH = "/home/whahn/projects/lumia-kenkyu/src/matches/output_examples/archive"
ERROR_PATH = os.path.join(os.path.dirname(ARCHIVE_PATH), "error")

BASE_URL = "https://open-api.bser.io/"
CURRENT_SEASON = 25  # Season 4 "SUNSET"
HEADERS = {
    "Accept": "application/json",
    "x-api-key": get_provider_secrets(DBProvider.API_ONLY),
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
