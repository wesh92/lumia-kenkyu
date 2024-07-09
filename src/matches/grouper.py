from collections import defaultdict
import json
from pydantic import BaseModel
from typing import List, Dict
import os
from models.game import UserGame
from getter import _fetch_multiple_games

def group_by_team(user_games: List[UserGame]) -> Dict[int, List[UserGame]]:
    """
    Group UserGame objects by team_id.

    :param user_games: List of UserGame objects
    :return: Dictionary with team_id as key and list of UserGame objects as value
    """
    teams = defaultdict(list)
    for game in user_games:
        teams[game.team_id].append(game)
    return dict(teams)

def write_teams_to_json(grouped_teams: Dict[int, List[UserGame]], output_dir: str):
    """
    Write grouped team data to JSON files.

    :param grouped_teams: Dictionary with team_id as key and list of UserGame objects as value
    :param output_dir: Directory to write JSON files to
    """
    os.makedirs(output_dir, exist_ok=True)

    for team_id, team_data in grouped_teams.items():
        filename = os.path.join(output_dir, f"team_{team_id}.json")

        # Convert UserGame objects to dictionaries
        team_data_dict = [game.model_dump() for game in team_data]

        with open(filename, 'w') as f:
            json.dump(team_data_dict, f, indent=2, default=str)  # Use default=str to handle datetime objects

# Usage example
game_ids = [36878649]  # Add your game IDs here
user_games = _fetch_multiple_games(game_ids)
grouped_teams = group_by_team(user_games)
write_teams_to_json(grouped_teams, "output_examples")
