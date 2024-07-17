from collections import Counter
from typing import Any
from models.game import UserGame
from data_access.supabase import SupabaseDAO


class GameDataService:
    def __init__(self):
        self.dao = SupabaseDAO()

    def process_game_data(self, game_data: UserGame):
        game_id = game_data.game_id

        if not self.dao.game_exists(game_id):
            game_insert = self._prepare_game_insert(game_data)
            self.dao.insert_game(game_insert)

        if not self.dao.player_game_stats_exist(game_id, game_data.user_id):
            player_stats = self._prepare_player_stats(game_data)
            self.dao.insert_player_stats(player_stats)

            mastery_inserts = self._prepare_mastery_inserts(game_data)
            self.dao.insert_mastery_levels(mastery_inserts)

            equipment_inserts = self._prepare_equipment_inserts(game_data)
            self.dao.insert_equipment(equipment_inserts)

            skill_inserts = self._prepare_skill_inserts(game_data)
            self.dao.insert_skill_order(skill_inserts)

            killed_by_inserts = self._prepare_killed_by_inserts(game_data)
            self.dao.insert_killed_by_data(killed_by_inserts)

            item_purchases = self._prepare_item_purchases(game_data)
            self.dao.insert_items_purchased(item_purchases)

    def _prepare_game_insert(self, game_data: UserGame) -> dict[str, Any]:
        return {
            "game_id": game_data.game_id,
            "game_start_time": game_data.game_start_datetime.isoformat(),
            "season_id": game_data.season_id,
            "match_mode": game_data.match_mode,
            "match_team_mode": game_data.match_team_mode,
            "server": game_data.server,
            "duration": game_data.duration,
            "total_match_players": game_data.total_match_players,
            "main_weather_code": game_data.main_weather,
            "sub_weather_code": game_data.sub_weather,
        }

    def _prepare_player_stats(self, game_data: UserGame) -> dict[str, Any]:
        return {
            "game_id": game_data.game_id,
            "game_start_time": game_data.game_start_datetime.isoformat(),
            "user_id": game_data.user_id,
            "nickname": game_data.nickname,
            "character_id": game_data.character_id,
            "team_id": game_data.team_id,
            "game_place_result": game_data.game_place_result,
            "level": game_data.level,
            "kills": game_data.kills,
            "assists": game_data.assists,
            "monster_kills": game_data.monster_kills,
            "damage_to_player": game_data.damage_to_player,
            "damage_to_monster": game_data.damage_to_monster,
            "tanked_damage": game_data.tanked_damage,
            "healing": game_data.healing,
            "victory": game_data.victory,
            "mmr_change": game_data.mmr_change,
            "mmr_before": game_data.mmr_before,
            "mmr_gain": game_data.mmr_gain,
            "mmr_after": game_data.mmr_after,
            "starting_area": game_data.starting_area,
            "deaths": game_data.deaths,
            "double_kills": game_data.double_kills,
            "triple_kills": game_data.triple_kills,
            "quadra_kills": game_data.quadra_kills,
            "extra_kills": game_data.extra_kills,
            "possessed_credits": game_data.posessed_credits,
            "used_credits": game_data.used_credits,
        }

    def _prepare_mastery_inserts(self, game_data: UserGame) -> list[dict[str, Any]]:
        return [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "mastery_type": int(mastery_type),
                "level": level,
            }
            for mastery_type, level in game_data.final_mastery_levels.items()
        ]

    def _prepare_equipment_inserts(self, game_data: UserGame) -> list[dict[str, Any]]:
        final_equipment = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "slot": int(slot),
                "item_id": item_id,
                "type": 2,  # Final equipment
            }
            for slot, item_id in game_data.final_equipment.items()
        ]

        first_equipment = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "slot": int(slot),
                "item_id": item_id[0],
                "type": 1,  # First equipment
            }
            for slot, item_id in game_data.equipment_first_item.items()
        ]

        return final_equipment + first_equipment

    def _prepare_skill_inserts(self, game_data: UserGame) -> list[dict[str, Any]]:
        return [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "skill_level": int(skill_level),
                "skill_id": skill_id,
            }
            for skill_level, skill_id in game_data.skill_order.items()
        ]

    def _prepare_killed_by_inserts(self, game_data: UserGame) -> list[dict[str, Any]]:
        return [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "killed_by_id": kill_data.killed_by_id,
                "killed_by_type": kill_data.killed_by_type,
                "killed_by_name": kill_data.killed_by_name,
                "died_area": kill_data.died_area,
                "killed_by_character": kill_data.killed_by_character,
                "killed_by_character_weapon": kill_data.killed_by_character_weapon,
            }
            for kill_data in game_data.killed_by_data.root
        ]

    def _prepare_item_purchases(self, game_data: UserGame) -> list[dict[str, Any]]:
        console_items = Counter(game_data.items_purchased_from_console)
        drone_items = Counter(game_data.items_purchased_from_drone)

        console_purchases = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "item_id": item_id,
                "purchase_type": "console",
                "quantity": quantity,
            }
            for item_id, quantity in console_items.items()
        ]

        drone_purchases = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "item_id": item_id,
                "purchase_type": "drone",
                "quantity": quantity,
            }
            for item_id, quantity in drone_items.items()
        ]

        return console_purchases + drone_purchases
