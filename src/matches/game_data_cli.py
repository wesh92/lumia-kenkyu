import typer
import requests
from typing import Optional
from models.game import UserGame
from data_access.supabase import SupabaseDAO
from processors.prepare_processors import GameDataService
from processors.insertion_processors import (
    DataInsertionContext,
    AllDataInsertionStrategy,
)
from CONSTS import (
    MATCHES_PATH,
    ARCHIVE_PATH,
    ERROR_PATH,
    BASE_URL,
    version,
    endpoints,
    HEADERS,
    CURRENT_SEASON,
)
import os
import shutil
import json
import random
from time import sleep
from collections import defaultdict
from getter import _fetch_by_game_id, _fetch_user_id_by_username

app = typer.Typer()
dao = SupabaseDAO()
game_service = GameDataService()


def fetch_user_games(
    user_id: int, next_id: Optional[int] = None
) -> tuple[list[UserGame], Optional[int]]:
    endpoint = endpoints.user.value["fetch_user_games"].format(user_id=user_id)
    url = f"{BASE_URL}{version.v1.value}/{endpoint}"
    if next_id:
        url += f"?next={next_id}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    games = []
    for game_data in data.get("userGames", []):
        try:
            game = UserGame(**game_data)
            games.append(game)
        except Exception as e:
            typer.echo(f"Error creating UserGame object: {str(e)}")
            typer.echo(f"Problematic game data: {game_data}")
            continue

    return games, data.get("next")


def get_user_id(username: str) -> Optional[int]:
    user = dao.get_user_by_nickname(username)
    if user:
        return user["user_id"]

    # If not found, fetch from API and insert

    user = _fetch_user_id_by_username(username)
    if user:
        user_data = {"user_id": user.user_id, "nickname": user.nickname}
        dao.insert_user(user_data)
        return user.user_id

    return None


def group_by_team(user_games: list[UserGame]) -> dict[int, list[UserGame]]:
    """Group UserGame objects by team_id."""
    teams = defaultdict(list)
    for game in user_games:
        teams[game.team_id].append(game)
    return dict(teams)


def write_teams_to_json(
    grouped_teams: dict[int, list[UserGame]], output_dir: str, game_id: int
):
    """Write grouped team data to JSON files."""
    os.makedirs(output_dir, exist_ok=True)

    for team_id, team_data in grouped_teams.items():
        filename = os.path.join(output_dir, f"{str(game_id)}/team_{team_id}.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        team_data_dict = [game.model_dump() for game in team_data]

        with open(filename, "w") as f:
            json.dump(team_data_dict, f, indent=2, default=str)


def generate_game_ids(count: int) -> list[int]:
    """Generate unique game IDs."""
    game_ids = []
    for _ in range(count):
        random_part = random.randint(0, 999999)
        random_stem = random.choice([35, 36, 37])
        game_id = int(f"{random_stem}{random_part:06d}")
        game_ids.append(game_id)

    for root, dirs, files in os.walk(ARCHIVE_PATH):
        for d in dirs:
            if int(d) in game_ids:
                game_ids.remove(int(d))
                typer.echo(f"Game ID {d} is already in the archive, skipping...")

    return game_ids


def process_game(game_id: int) -> Optional[list[UserGame]]:
    """Process a single game by ID."""
    response = None
    try:
        response = _fetch_by_game_id(game_id)

        if isinstance(response, dict):
            if "userGames" not in response:
                typer.echo(
                    f"Game with ID {game_id} does not contain 'userGames' key. Response keys: {response.keys()}"
                )
                return None

            games = response["userGames"]
        else:
            games = response

        if not games:
            typer.echo(f"No data found for game ID {game_id}, skipping...")
            return None

        if games[0].season_id != CURRENT_SEASON and games[0].season_id != 0:
            typer.echo(
                f"Game with ID {game_id} is not from the current season or season 0. From season ID {games[0].season_id}, skipping..."
            )
            return None

        has_weather_data = any(
            getattr(game, "main_weather", None) is not None
            and getattr(game, "sub_weather", None) is not None
            for game in games
        )
        if not has_weather_data:
            typer.echo(f"Game with ID {game_id} has no weather data, skipping...")
            return None

        return games

    except Exception as e:
        typer.echo(f"Error processing game with ID {game_id}: {str(e)}")
        if response is not None:
            typer.echo(f"Response content: {json.dumps(response, indent=2)}")
        else:
            typer.echo("No response received from API.")
        return None


@app.command()
def insert_users(
    usernames: list[str] = typer.Argument(..., help="Username(s) to fetch and insert"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force update even if user exists"
    ),
):
    """Fetch user IDs by username(s) and insert them into the database."""
    for username in usernames:
        user = dao.get_user_by_nickname(username)
        if user and not force:
            typer.echo(f"User {username} already exists. Use --force to update.")
            continue

        fetched_user = _fetch_user_id_by_username(username)
        if fetched_user:
            user_data = {
                "user_id": fetched_user.user_id,
                "nickname": fetched_user.nickname,
            }
            dao.insert_user(user_data)
            typer.echo(f"Inserted/Updated user: {username}")
        else:
            typer.echo(f"Failed to fetch data for username: {username}")


@app.command()
def fetch_user_games_command(
    username: str = typer.Argument(..., help="Username to fetch games for"),
    limit: int = typer.Option(10, help="Maximum number of games to fetch"),
):
    """Fetch and insert user games data for a given username."""
    user_id = get_user_id(username)
    if not user_id:
        typer.echo(f"Failed to find or fetch user ID for username: {username}")
        return

    next_id = None
    games_processed = 0
    insertion_context = DataInsertionContext(AllDataInsertionStrategy())

    while games_processed < limit:
        games, next_id = fetch_user_games(user_id, next_id)

        for game in games:
            if not dao.game_exists(game.game_id) or not dao.player_game_stats_exist(
                game.game_id, user_id
            ):
                insertion_context.insert_data(game, dao)
                games_processed += 1
                typer.echo(f"Inserted game data for game ID: {game.game_id}")
            else:
                typer.echo(
                    f"Game {game.game_id} already exists for user {username}. Skipping."
                )

            if games_processed >= limit:
                break

        if not next_id:
            break

    typer.echo(f"Processed {games_processed} games for user {username}")


@app.command()
def process_json_files(
    directory: str = typer.Option(
        MATCHES_PATH, help="Directory containing JSON files to process"
    ),
    archive_dir: str = typer.Option(
        ARCHIVE_PATH, help="Directory to move processed files"
    ),
    error_dir: str = typer.Option(
        ERROR_PATH, help="Directory to move files with errors"
    ),
):
    """Process JSON files in the specified directory and insert data into the database."""
    insertion_context = DataInsertionContext(AllDataInsertionStrategy())

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        game_data = json.load(f)
                    for player_data in game_data:
                        game = UserGame(**player_data)
                        insertion_context.insert_data(game, dao)
                    shutil.move(file_path, os.path.join(archive_dir, file))
                    typer.echo(f"Processed and archived: {file}")
                except Exception as e:
                    typer.echo(f"Error processing {file}: {str(e)}")
                    shutil.move(file_path, os.path.join(error_dir, file))


@app.command()
def process_single_file(
    file_path: str = typer.Argument(..., help="Path to a single JSON file to process"),
    archive_dir: str = typer.Option(
        ARCHIVE_PATH, help="Directory to move processed file"
    ),
    error_dir: str = typer.Option(
        ERROR_PATH, help="Directory to move file if processing fails"
    ),
):
    """Process a single JSON file and insert data into the database."""
    insertion_context = DataInsertionContext(AllDataInsertionStrategy())

    try:
        with open(file_path, "r") as f:
            game_data = json.load(f)
        for player_data in game_data:
            game = UserGame(**player_data)
            insertion_context.insert_data(game, dao)
        shutil.move(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
        typer.echo(f"Processed and archived: {file_path}")
    except Exception as e:
        typer.echo(f"Error processing {file_path}: {str(e)}")
        shutil.move(file_path, os.path.join(error_dir, os.path.basename(file_path)))


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
    """Generate game IDs, process games, and write team data to JSON files."""
    game_ids = generate_game_ids(count)

    for i, game_id in enumerate(game_ids, 1):
        typer.echo(f"Processing game number {i} of {len(game_ids)}")
        typer.echo(f"Processing game ID: {game_id}")
        games = process_game(game_id)
        if games:
            grouped_teams = group_by_team(games)
            write_teams_to_json(grouped_teams, output_dir, game_id)
            sleep(delay)


if __name__ == "__main__":
    app()
