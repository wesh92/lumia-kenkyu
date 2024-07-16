import threading
from supabase import create_client, Client
from CONSTS import SUPABASE_URL, SUPABASE_KEY
from typing import Optional, Any


class SupabaseDAO:
    _instance: Optional["SupabaseDAO"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "SupabaseDAO":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__initialize()
        return cls._instance

    def __initialize(self) -> None:
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Game-related methods
    def insert_game(self, game_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.table("games").upsert(game_data).execute()

    def game_exists(self, game_id: int) -> bool:
        result = (
            self.client.table("games")
            .select("game_id")
            .eq("game_id", game_id)
            .execute()
        )
        return bool(result.data)

    # Player game stats methods
    def insert_player_stats(self, player_stats: dict[str, Any]) -> dict[str, Any]:
        return self.client.table("player_game_stats").upsert(player_stats).execute()

    def player_game_stats_exist(self, game_id: int, user_id: int) -> bool:
        result = (
            self.client.table("player_game_stats")
            .select("game_id")
            .eq("game_id", game_id)
            .eq("user_id", user_id)
            .execute()
        )
        return bool(result.data)

    # Mastery levels methods
    def insert_mastery_levels(
        self, mastery_inserts: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return self.client.table("mastery_levels").upsert(mastery_inserts).execute()

    # Equipment methods
    def insert_equipment(
        self, equipment_inserts: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return self.client.table("equipment").upsert(equipment_inserts).execute()

    # Skill order methods
    def insert_skill_order(self, skill_inserts: list[dict[str, Any]]) -> dict[str, Any]:
        return self.client.table("skill_order").upsert(skill_inserts).execute()

    # Killed by data methods
    def insert_killed_by_data(
        self, killed_by_inserts: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return self.client.table("killed_by_data").upsert(killed_by_inserts).execute()

    # Items purchased methods
    def insert_items_purchased(
        self, item_purchases: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return self.client.table("items_purchased").upsert(item_purchases).execute()

    # User-related methods
    def insert_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.table("users").upsert(user_data).execute()

    def get_user_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        result = (
            self.client.table("users").select("*").eq("nickname", nickname).execute()
        )
        return result.data[0] if result.data else None

    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        result = self.client.table("users").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None

    # Generic select method for flexibility
    def select(self, table: str, columns: str = "*", **filters) -> list[dict[str, Any]]:
        query = self.client.table(table).select(columns)
        for key, value in filters.items():
            query = query.eq(key, value)
        result = query.execute()
        return result.data

    # Generic upsert method for flexibility
    def upsert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.client.table(table).upsert(data).execute()

    # Method to handle batch operations
    def batch_insert(
        self, table: str, data_list: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return self.client.table(table).upsert(data_list).execute()
