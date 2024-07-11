import json
from supabase import create_client, Client
from datetime import datetime
from collections import Counter
import os
import shutil
from CONSTS import MATCHES_PATH, SUPABASE_KEY, SUPABASE_URL, ARCHIVE_PATH, ERROR_PATH
import concurrent.futures
import threading

# Initialize Supabase client
supabase_url = SUPABASE_URL
supabase_key = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Thread-local storage for Supabase clients
local = threading.local()


def get_supabase_client():
    if not hasattr(local, "supabase"):
        local.supabase = create_client(supabase_url, supabase_key)
    return local.supabase


def datetime_parser(json_dict):
    for key, value in json_dict.items():
        if key == "game_start_datetime":
            try:
                json_dict[key] = datetime.fromisoformat(
                    value.replace("+0900", "+09:00")
                )
            except:  # noqa: E722
                pass
    return json_dict


def insert_game_data(json_data: str):
    supabase = get_supabase_client()
    # Parse JSON data with custom parser for datetime
    game_data = json.loads(json_data, object_hook=datetime_parser)

    # Extract game_start_time from the first player's data
    game_start_time = game_data[0]["game_start_datetime"]
    game_id = game_data[0]["game_id"]

    # Check if the game already exists
    existing_game = supabase.table("games").select("*").eq("game_id", game_id).execute()

    if len(existing_game.data) == 0:
        # Game doesn't exist, insert it
        game_insert = {
            "game_id": game_id,
            "game_start_time": game_start_time.isoformat(),
            "season_id": game_data[0]["season_id"],
            "match_mode": game_data[0]["match_mode"],
            "match_team_mode": game_data[0]["match_team_mode"],
            "server": game_data[0]["server"],
            "duration": game_data[0]["duration"],
            "total_match_players": game_data[0]["total_match_players"],
            "main_weather_code": game_data[0]["main_weather"],
            "sub_weather_code": game_data[0]["sub_weather"],
        }
        supabase.table("games").upsert(game_insert).execute()
        print(f"Inserted new game data for game {game_id}")
    else:
        print(f"Game {game_id} already exists, skipping game insertion")

    # Insert player game stats and related data
    for player in game_data:
        # Check if player stats already exist
        existing_stats = (
            supabase.table("player_game_stats")
            .select("*")
            .eq("game_id", game_id)
            .eq("user_id", player["user_id"])
            .execute()
        )

        if len(existing_stats.data) == 0:
            # Player stats don't exist, insert them
            player_stats = {
                "game_id": game_id,
                "game_start_time": game_start_time.isoformat(),
                "user_id": player["user_id"],
                "nickname": player["nickname"],
                "character_id": player["character_id"],
                "team_id": player["team_id"],
                "game_place_result": player["game_place_result"],
                "level": player["level"],
                "kills": player["kills"],
                "assists": player["assists"],
                "monster_kills": player["monster_kills"],
                "damage_to_player": player["damage_to_player"],
                "damage_to_monster": player["damage_to_monster"],
                "tanked_damage": player["tanked_damage"],
                "healing": player["healing"],
                "victory": player["victory"],
                "mmr_change": player["mmr_change"],
                "mmr_before": player["mmr_before"],
                "mmr_gain": player["mmr_gain"],
                "mmr_after": player["mmr_after"],
                "starting_area": player["starting_area"],
                "deaths": player["deaths"],
                "double_kills": player["double_kills"],
                "triple_kills": player["triple_kills"],
                "quadra_kills": player["quadra_kills"],
                "extra_kills": player["extra_kills"],
                "possessed_credits": player["posessed_credits"],
                "used_credits": player["used_credits"],
            }
            supabase.table("player_game_stats").upsert(player_stats).execute()
            print(
                f"Inserted player stats for user {player['user_id']} in game {game_id}"
            )

            # Insert mastery_levels
            mastery_inserts = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "mastery_type": int(mastery_type),
                    "level": level,
                }
                for mastery_type, level in player["final_mastery_levels"].items()
            ]
            supabase.table("mastery_levels").upsert(mastery_inserts).execute()
            print(f"Inserted mastery levels for user {player['user_id']} in game {game_id}")

            # Insert equipment
            equipment_inserts = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "slot": int(slot),
                    "item_id": item_id,
                    "type": 2 # Final equipment (equipment the user died/won with)
                }
                for slot, item_id in player["final_equipment"].items()
            ]
            supabase.table("equipment").upsert(equipment_inserts).execute()
            print(f"Inserted final equipment for user {player['user_id']} in game {game_id}")

            # Insert for equipment_first_item (first purchased items)
            equipment_first_item_inserts = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "slot": int(slot),
                    "item_id": item_id[0],
                    "type": 1 # Phase 1 items (usually referred to as purples)
                }
                for slot, item_id in player["equipment_first_item"].items()
            ]
            supabase.table("equipment").upsert(equipment_first_item_inserts).execute()
            print(f"Inserted first equipment for user {player['user_id']} in game {game_id}")

            # Insert skill_order
            skill_inserts = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "skill_level": int(skill_level),
                    "skill_id": skill_id,
                }
                for skill_level, skill_id in player["skill_order"].items()
            ]
            supabase.table("skill_order").upsert(skill_inserts).execute()
            print(f"Inserted skill order for user {player['user_id']} in game {game_id}")

            # Insert killed_by_data
            killed_by_inserts = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "killed_by_id": kill_data["killed_by_id"],
                    "killed_by_type": kill_data["killed_by_type"],
                    "killed_by_name": kill_data["killed_by_name"],
                    "died_area": kill_data["died_area"],
                    "killed_by_character": kill_data["killed_by_character"],
                    "killed_by_character_weapon": kill_data[
                        "killed_by_character_weapon"
                    ],
                }
                for kill_data in player["killed_by_data"]
            ]
            supabase.table("killed_by_data").upsert(killed_by_inserts).execute()
            print(f"Inserted killed by data for user {player['user_id']} in game {game_id}")

            # Insert items_purchased
            console_items = Counter(player["items_purchased_from_console"])
            drone_items = Counter(player["items_purchased_from_drone"])

            item_purchases = [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "item_id": item_id,
                    "purchase_type": "console",
                    "quantity": quantity,
                }
                for item_id, quantity in console_items.items()
            ] + [
                {
                    "game_start_time": game_start_time.isoformat(),
                    "game_id": game_id,
                    "user_id": player["user_id"],
                    "item_id": item_id,
                    "purchase_type": "drone",
                    "quantity": quantity,
                }
                for item_id, quantity in drone_items.items()
            ]
            supabase.table("items_purchased").upsert(item_purchases).execute()

            print(
                f"Inserted all related data for user {player['user_id']} in game {game_id}"
            )
        else:
            print(
                f"Player stats for user {player['user_id']} in game {game_id} already exists, skipping insertion"
            )

    print(f"Finished processing data for game {game_id}")


def move_to_archive(game_folder):
    """
    Move the processed game folder to the archive directory.

    :param game_folder: Path to the game folder
    """
    archive_path = os.path.join(ARCHIVE_PATH, os.path.basename(game_folder))
    try:
        shutil.move(game_folder, archive_path)
        print(f"Moved {game_folder} to {archive_path}")
    except Exception as e:
        print(f"Error moving {game_folder} to archive: {str(e)}")


def move_to_error(game_folder):
    """
    Move the game folder with processing errors to the error directory.

    :param game_folder: Path to the game folder
    """
    error_path = os.path.join(ERROR_PATH, os.path.basename(game_folder))
    try:
        os.makedirs(ERROR_PATH, exist_ok=True)
        shutil.move(game_folder, error_path)
        print(f"Moved {game_folder} to error directory: {error_path}")
    except Exception as e:
        print(f"Error moving {game_folder} to error directory: {str(e)}")


def process_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            json_data = f.read()
        insert_game_data(json_data)
        print(f"Processed file: {file_path}")
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return False


def process_json_files(directory):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ["archive", "error"]]
            json_files = [f for f in files if f.endswith(".json")]
            if json_files:
                game_folder = root
                file_paths = [os.path.join(root, file) for file in json_files]

                # Submit all file processing tasks and wait for them to complete
                futures = [
                    executor.submit(process_json_file, file_path)
                    for file_path in file_paths
                ]
                results = [
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                ]

                if all(results):
                    move_to_archive(game_folder)
                else:
                    print(
                        f"Some files in {game_folder} failed to process. Moving to error directory."
                    )
                    move_to_error(game_folder)


if __name__ == "__main__":
    # Usage example
    output_dir = MATCHES_PATH
    process_json_files(output_dir)
