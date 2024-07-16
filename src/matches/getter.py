import requests
import CONSTS
from models.game import UserGame, KillData, KillDataList
from models.user import User
from datetime import datetime
from typing import Optional


def _fetch_by_user_id(
    user_id: int, next_id: Optional[int] = None
) -> tuple[list[UserGame], Optional[int]]:
    try:
        endpoint = CONSTS.endpoints.user.value["fetch_user_games"].format(
            user_id=user_id
        )
        url = f"{CONSTS.BASE_URL}{CONSTS.version.v1.value}/{endpoint}"
        if next_id:
            url += f"?next={next_id}"

        response = requests.get(url, headers=CONSTS.HEADERS)
        response.raise_for_status()
        game_data = response.json()

        user_games: list[UserGame] = []

        for game in game_data["userGames"]:
            # Create KillData objects
            kill_data_list = []
            for i in range(1, 4):  # Up to 3 sets of kill data
                killer_prefix = "" if i == 1 else f"{i}"
                if f"killer{killer_prefix}" in game:
                    kill_data = KillData(
                        killerUserNum=game.get(f"killerUserNum{killer_prefix}", 0),
                        killer=game.get(f"killer{killer_prefix}", ""),
                        killDetail=game.get(f"killDetail{killer_prefix}", ""),
                        placeOfDeath=game.get(f"placeOfDeath{killer_prefix}", ""),
                        killerCharacter=game.get(f"killerCharacter{killer_prefix}", ""),
                        killerWeapon=game.get(f"killerWeapon{killer_prefix}", ""),
                    )
                    kill_data_list.append(kill_data)
                    # Convert game_start_datetime to datetime object
            game["startDtm"] = datetime.fromisoformat(
                game["startDtm"].replace("+0900", "+09:00")
            )

            # Ensure equipment data is present
            if "equipment" not in game:
                game["equipment"] = {}
            if "equipFirstItemForLog" not in game:
                game["equipFirstItemForLog"] = {}

            # Create UserGame object
            user_game = UserGame(
                **game,
                killerList=KillDataList(root=kill_data_list),
                # equipment=player_data["equipment"],
                # equipFirstItemForLog=player_data["equipFirstItemForLog"]
            )
            user_games.append(user_game)

            return user_games, game_data.get("next", None)
    except requests.RequestException as e:
        print(f"Error fetching game data for user ID {user_id}: {str(e)}")
        return list(), None
    except KeyError as e:
        print(f"Unexpected response format for user ID {user_id}: {str(e)}")
        return list(), None
    except Exception as e:
        print(f"Unexpected error processing user ID {user_id}: {str(e)}")
        return list(), None


def _fetch_by_game_id(game_id: int) -> list[UserGame]:
    """
    Internal function to fetch game data by game id and convert to UserGame objects.

    :param game_id: int
    :return: List[UserGame]
    """
    try:
        endpoint = CONSTS.endpoints.game.value["fetch_by_id"].format(game_id=game_id)
        response = requests.get(
            f"{CONSTS.BASE_URL}{CONSTS.version.v1.value}/{endpoint}",
            headers=CONSTS.HEADERS,
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch game data by game id: {game_id}")

        game_data = response.json()
        user_games = []
        for player_data in game_data["userGames"]:
            # Create KillData objects
            kill_data_list = []
            for i in range(1, 4):  # Up to 3 sets of kill data
                killer_prefix = "" if i == 1 else f"{i}"
                if f"killer{killer_prefix}" in player_data:
                    kill_data = KillData(
                        killerUserNum=player_data.get(
                            f"killerUserNum{killer_prefix}", 0
                        ),
                        killer=player_data.get(f"killer{killer_prefix}", ""),
                        killDetail=player_data.get(f"killDetail{killer_prefix}", ""),
                        placeOfDeath=player_data.get(
                            f"placeOfDeath{killer_prefix}", ""
                        ),
                        killerCharacter=player_data.get(
                            f"killerCharacter{killer_prefix}", ""
                        ),
                        killerWeapon=player_data.get(
                            f"killerWeapon{killer_prefix}", ""
                        ),
                    )
                    kill_data_list.append(kill_data)

            # Convert game_start_datetime to datetime object
            player_data["startDtm"] = datetime.fromisoformat(
                player_data["startDtm"].replace("+0900", "+09:00")
            )

            # Ensure equipment data is present
            if "equipment" not in player_data:
                player_data["equipment"] = {}
            if "equipFirstItemForLog" not in player_data:
                player_data["equipFirstItemForLog"] = {}

            # Create UserGame object
            user_game = UserGame(
                **player_data,
                killerList=KillDataList(root=kill_data_list),
                # equipment=player_data["equipment"],
                # equipFirstItemForLog=player_data["equipFirstItemForLog"]
            )
            user_games.append(user_game)

        return user_games
    except requests.RequestException as e:
        print(f"Error fetching game data for game ID {game_id}: {str(e)}")
        return list()
    except KeyError as e:
        print(f"Unexpected response format for game ID {game_id}: {str(e)}")
        return list()
    except Exception as e:
        print(f"Unexpected error processing game ID {game_id}: {str(e)}")
        return list()


def _fetch_multiple_games(game_ids: list[int]) -> list[UserGame]:
    """
    Fetch data for multiple games and return a list of UserGame objects.

    :param game_ids: list of game IDs to fetch
    :return: list of UserGame objects
    """
    all_user_games = []
    for game_id in game_ids:
        all_user_games.extend(_fetch_by_game_id(game_id))
    return all_user_games


def _fetch_user_id_by_username(username: str) -> User:
    """
    Fetch user ID by username and return a User object.

    :param username: str
    :return: User
    """
    try:
        endpoint = CONSTS.endpoints.user.value["fetch_by_username"]
        response = requests.get(
            f"{CONSTS.BASE_URL}{CONSTS.version.v1.value}/{endpoint}",
            headers=CONSTS.HEADERS,
            params={"query": username},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user ID by username: {username}")

        user_data = response.json()["user"]
        user = User(**user_data)
        return user
    except requests.RequestException as e:
        print(f"Error fetching user ID for username {username}: {str(e)}")
        return None
    except KeyError as e:
        print(f"Unexpected response format for username {username}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error processing username {username}: {str(e)}")
        return None
