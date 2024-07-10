import typer
from collections import defaultdict
import json
import os
from models.game import UserGame
from getter import _fetch_by_game_id
import random
from time import sleep
from CONSTS import CURRENT_SEASON

app = typer.Typer()


def group_by_team(user_games: list[UserGame]) -> dict[int, list[UserGame]]:
    """
    Group UserGame objects by team_id.

    :param user_games: List of UserGame objects
    :return: Dictionary with team_id as key and list of UserGame objects as value
    """
    teams = defaultdict(list)
    for game in user_games:
        teams[game.team_id].append(game)
    return dict(teams)


def write_teams_to_json(
    grouped_teams: dict[int, list[UserGame]], output_dir: str, game_id: int
):
    """
    Write grouped team data to JSON files.

    :param grouped_teams: Dictionary with team_id as key and list of UserGame objects as value
    :param output_dir: Directory to write JSON files to
    """
    os.makedirs(output_dir, exist_ok=True)

    for team_id, team_data in grouped_teams.items():
        filename = os.path.join(output_dir, f"{str(game_id)}/team_{team_id}.json")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Convert UserGame objects to dictionaries
        team_data_dict = [game.model_dump() for game in team_data]

        with open(filename, "w") as f:
            json.dump(
                team_data_dict, f, indent=2, default=str
            )  # Use default=str to handle datetime objects


def generate_game_ids(count) -> list[int]:
    game_ids = []
    for _ in range(count):
        # Generate a random 6-digit number
        random_part = random.randint(0, 999999)
        # Combine '36' with the random part, ensuring it's 8 digits long
        game_id = int(f"36{random_part:06d}")
        game_ids.append(game_id)
    return game_ids


def process_game(game_id):
    response = None
    try:
        response = _fetch_by_game_id(game_id)

        if isinstance(response, dict):
            if 'userGames' not in response:
                print(f"Game with ID {game_id} does not contain 'userGames' key. Response keys: {response.keys()}")
                return None

            games = response['userGames']
        else:
            games = response

        if not games:
            print(f"No data found for game ID {game_id}, skipping...")
            return None

        if games[0].season_id != CURRENT_SEASON and games[0].season_id != 0:
            print(f"Game with ID {game_id} is not from the current season or season 0. From season ID {games[0].season_id}, skipping...")
            return None

        # Check if any game in the list has weather data
        has_weather_data = any(getattr(game, 'main_weather', None) is not None and
                               getattr(game, 'sub_weather', None) is not None
                               for game in games)
        if not has_weather_data:
            print(f"Game with ID {game_id} has no weather data, skipping...")
            return None

        return games

    except Exception as e:
        print(f"Error processing game with ID {game_id}: {str(e)}")
        if response is not None:
            print(f"Response content: {json.dumps(response, indent=2)}")
        else:
            print("No response received from API.")
        return None


@app.command()
def process_games(
    count: int = typer.Option(100, help="Number of game IDs to generate and process"),
    output_dir: str = typer.Option(
        "output_examples", help="Directory to write output JSON files"
    ),
    delay: float = typer.Option(
        1.33, help="Delay in seconds between processing each game"
    ),
):
    """
    Generate game IDs, process games, and write team data to JSON files.
    """
    game_ids = generate_game_ids(count)

    for i, game_id in enumerate(game_ids, 1):
        print(f"Processing game number {i} of {len(game_ids)}")
        print(f"Processing game ID: {game_id}")
        games = process_game(game_id)
        if games:
            grouped_teams = group_by_team(games)
            write_teams_to_json(grouped_teams, output_dir, game_id)
            sleep(delay)


if __name__ == "__main__":
    app()
