from typing import Any, Optional, Sequence
from supabase import create_client, Client
from data_access.dao import AbstractDAO
from CONSTS import SUPABASE_URL, SUPABASE_KEY


class SupabaseDAO(AbstractDAO):
    """
    Supabase implementation of the AbstractDAO.
    Provides methods to interact with a Supabase database.
    """

    def __init__(self):
        """Initialize the SupabaseDAO."""
        self.client: Client

    def initialize(self) -> None:
        """Initialize the Supabase client."""
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def insert_game(self, game_data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new game record into the Supabase database."""
        return self.client.table("games").upsert(game_data).execute().data

    def game_exists(self, game_id: int) -> bool:
        """Check if a game with the given ID exists in the Supabase database."""
        result = (
            self.client.table("games")
            .select("game_id")
            .eq("game_id", game_id)
            .execute()
        )
        return bool(result.data)

    def insert_player_stats(self, player_stats: dict[str, Any]) -> dict[str, Any]:
        """Insert player statistics for a game into the Supabase database."""
        return (
            self.client.table("player_game_stats").upsert(player_stats).execute().data
        )

    def player_game_stats_exist(self, game_id: int, user_id: int) -> bool:
        """Check if player statistics exist for a given game and user in the Supabase database."""
        result = (
            self.client.table("player_game_stats")
            .select("game_id")
            .eq("game_id", game_id)
            .eq("user_id", user_id)
            .execute()
        )
        return bool(result.data)

    def insert_mastery_levels(
        self, mastery_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert mastery levels data into the Supabase database."""
        return (
            self.client.table("mastery_levels")
            .upsert(
                mastery_inserts,
                on_conflict="game_start_time,game_id,user_id,mastery_type",
            )
            .execute()
            .data
        )

    def insert_equipment(
        self, equipment_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert equipment data into the Supabase database."""
        return (
            self.client.table("equipment")
            .upsert(
                equipment_inserts, on_conflict="game_start_time,game_id,user_id,slot"
            )
            .execute()
            .data
        )

    def insert_skill_order(
        self, skill_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert skill order data into the Supabase database."""
        return (
            self.client.table("skill_order")
            .upsert(
                skill_inserts, on_conflict="game_start_time,game_id,user_id,skill_level"
            )
            .execute()
            .data
        )

    def insert_killed_by_data(
        self, killed_by_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert 'killed by' data into the Supabase database."""
        return (
            self.client.table("killed_by_data")
            .upsert(
                killed_by_inserts,
                on_conflict="game_start_time,game_id,user_id,killed_by_id",
            )
            .execute()
            .data
        )

    def insert_items_purchased(
        self, item_purchases: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert data about items purchased into the Supabase database."""
        return (
            self.client.table("items_purchased")
            .upsert(
                item_purchases,
                on_conflict="game_start_time,game_id,user_id,item_id,purchase_type",
            )
            .execute()
            .data
        )

    def insert_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new user record into the Supabase database."""
        return self.client.table("users").upsert(user_data).execute().data

    def get_user_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        """Retrieve a user record by their nickname from the Supabase database."""
        result = (
            self.client.table("users").select("*").eq("nickname", nickname).execute()
        )
        return result.data[0] if result.data else None

    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a user record by their user ID from the Supabase database."""
        result = self.client.table("users").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None

    def select(
        self, table: str, columns: str = "*", **filters: Any
    ) -> Sequence[dict[str, Any]]:
        """Perform a select operation on the specified table with given filters in the Supabase database."""
        query = self.client.table(table).select(columns)
        for key, value in filters.items():
            query = query.eq(key, value)
        result = query.execute()
        return result.data

    def upsert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Perform an upsert operation on the specified table in the Supabase database."""
        return self.client.table(table).upsert(data).execute().data

    def batch_insert(
        self, table: str, data_list: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Perform a batch insert operation on the specified table in the Supabase database."""
        return self.client.table(table).upsert(data_list).execute().data
