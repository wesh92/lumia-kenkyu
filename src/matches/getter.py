import requests
import CONSTS
from models.game import UserGame, KillData, KillDataList
from datetime import datetime

def _fetch_by_game_id(game_id: int) -> list[UserGame]:
    """
    Internal function to fetch game data by game id and convert to UserGame objects.

    :param game_id: int
    :return: List[UserGame]
    """
    endpoint = CONSTS.endpoints.game.value["fetch_by_id"].format(game_id=game_id)
    response = requests.get(f"{CONSTS.BASE_URL}{CONSTS.version.v1.value}/{endpoint}", headers=CONSTS.HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch game data by game id: {game_id}")

    game_data = response.json()
    user_games = []
    for player_data in game_data['userGames']:
        # Create KillData objects
        kill_data_list = []
        for i in range(1, 4):  # Up to 3 sets of kill data
            killer_prefix = '' if i == 1 else f'{i}'
            if f'killer{killer_prefix}' in player_data:
                kill_data = KillData(
                    killerUserNum=player_data.get(f'killerUserNum{killer_prefix}', 0),
                    killer=player_data.get(f'killer{killer_prefix}', ''),
                    killDetail=player_data.get(f'killDetail{killer_prefix}', ''),
                    placeOfDeath=player_data.get(f'placeOfDeath{killer_prefix}', ''),
                    killerCharacter=player_data.get(f'killerCharacter{killer_prefix}', ''),
                    killerWeapon=player_data.get(f'killerWeapon{killer_prefix}', '')
                )
                kill_data_list.append(kill_data)

        # Convert game_start_datetime to datetime object
        player_data['startDtm'] = datetime.fromisoformat(player_data['startDtm'].replace("+0900", "+09:00"))

        # Create UserGame object
        user_game = UserGame(**player_data, killerList=KillDataList(root=kill_data_list))
        user_games.append(user_game)

    return user_games

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
