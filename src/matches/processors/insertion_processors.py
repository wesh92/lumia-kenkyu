from abc import ABC, abstractmethod
from models.game import UserGame
from data_access.supabase import SupabaseDAO
from itertools import groupby
from operator import itemgetter
from collections import Counter


class InsertionStrategy(ABC):
    @abstractmethod
    def insert(self, game_data: UserGame, dao: SupabaseDAO) -> None:
        pass


class GameInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO) -> None:
        game_insert = {
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
        dao.insert_game(game_insert)


class PlayerStatsInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO) -> None:
        player_stats = {
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
        dao.insert_player_stats(player_stats)


class MasteryLevelsInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO):
        mastery_inserts = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "mastery_type": int(mastery_type),
                "level": level,
            }
            for mastery_type, level in game_data.final_mastery_levels.items()
        ]

        mastery_inserts.sort(
            key=itemgetter("game_start_time", "game_id", "user_id", "mastery_type")
        )
        unique_mastery = [
            next(group)
            for _, group in groupby(
                mastery_inserts,
                key=itemgetter("game_start_time", "game_id", "user_id", "mastery_type"),
            )
        ]

        if unique_mastery:
            dao.insert_mastery_levels(unique_mastery)


class EquipmentInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO):
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

        # Insert final equipment
        if final_equipment:
            dao.insert_equipment(final_equipment)

        # Insert first equipment
        if first_equipment:
            dao.insert_equipment(first_equipment)


class SkillOrderInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO):
        skill_inserts = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "skill_level": int(skill_level),
                "skill_id": skill_id,
            }
            for skill_level, skill_id in game_data.skill_order.items()
        ]

        skill_inserts.sort(
            key=itemgetter("game_start_time", "game_id", "user_id", "skill_level")
        )
        unique_skills = [
            next(group)
            for _, group in groupby(
                skill_inserts,
                key=itemgetter("game_start_time", "game_id", "user_id", "skill_level"),
            )
        ]

        if unique_skills:
            dao.insert_skill_order(unique_skills)


class KilledByDataInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO):
        killed_by_inserts = [
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

        # Sort and group by the primary key fields
        killed_by_inserts.sort(
            key=itemgetter("game_start_time", "game_id", "user_id", "killed_by_id")
        )
        unique_killed_by = [
            next(group)  # Take the first item from each group
            for _, group in groupby(
                killed_by_inserts,
                key=itemgetter("game_start_time", "game_id", "user_id", "killed_by_id"),
            )
        ]

        if unique_killed_by:
            dao.insert_killed_by_data(unique_killed_by)


class ItemPurchasesInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO):
        console_items = Counter(game_data.items_purchased_from_console)
        drone_items = Counter(game_data.items_purchased_from_drone)

        item_purchases = [
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "item_id": item_id,
                "purchase_type": "console",
                "quantity": quantity,
            }
            for item_id, quantity in console_items.items()
        ] + [
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

        item_purchases.sort(
            key=itemgetter(
                "game_start_time", "game_id", "user_id", "item_id", "purchase_type"
            )
        )
        unique_purchases = [
            next(group)
            for _, group in groupby(
                item_purchases,
                key=itemgetter(
                    "game_start_time", "game_id", "user_id", "item_id", "purchase_type"
                ),
            )
        ]

        if unique_purchases:
            dao.insert_items_purchased(unique_purchases)


class DataInsertionContext:
    def __init__(self, strategy: InsertionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: InsertionStrategy):
        self._strategy = strategy

    def insert_data(self, game_data: UserGame, dao: SupabaseDAO):
        self._strategy.insert(game_data, dao)


# Composite strategy to insert all data
class AllDataInsertionStrategy(InsertionStrategy):
    def insert(self, game_data: UserGame, dao: SupabaseDAO) -> None:
        strategies = [
            GameInsertionStrategy(),
            PlayerStatsInsertionStrategy(),
            MasteryLevelsInsertionStrategy(),
            EquipmentInsertionStrategy(),
            SkillOrderInsertionStrategy(),
            KilledByDataInsertionStrategy(),
            ItemPurchasesInsertionStrategy(),
        ]
        for strategy in strategies:
            strategy.insert(game_data, dao)
