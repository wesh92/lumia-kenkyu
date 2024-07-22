from abc import ABC, abstractmethod
from typing import Any, List, Optional
from collections.abc import Sequence


class AbstractDAO(ABC):
    """
    Abstract base class for Data Access Objects (DAOs).
    Defines the interface for database operations across different implementations.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the DAO with necessary setup."""
        pass

    @abstractmethod
    def insert_game(self, game_data: dict[str, Any]) -> dict[str, Any]:
        """
        Insert a new game record into the database.

        Args:
            game_data (dict[str, Any]): Dictionary containing game data.

        Returns:
            dict[str, Any]: The inserted game data, potentially with additional metadata.
        """
        pass

    @abstractmethod
    def game_exists(self, game_id: int) -> bool:
        """
        Check if a game with the given ID exists in the database.

        Args:
            game_id (int): The ID of the game to check.

        Returns:
            bool: True if the game exists, False otherwise.
        """
        pass

    @abstractmethod
    def insert_player_stats(self, player_stats: dict[str, Any]) -> dict[str, Any]:
        """
        Insert player statistics for a game into the database.

        Args:
            player_stats (dict[str, Any]): Dictionary containing player statistics.

        Returns:
            dict[str, Any]: The inserted player statistics, potentially with additional metadata.
        """
        pass

    @abstractmethod
    def player_game_stats_exist(self, game_id: int, user_id: int) -> bool:
        """
        Check if player statistics exist for a given game and user.

        Args:
            game_id (int): The ID of the game.
            user_id (int): The ID of the user.

        Returns:
            bool: True if statistics exist, False otherwise.
        """
        pass

    @abstractmethod
    def insert_mastery_levels(
        self, mastery_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Insert mastery levels data into the database.

        Args:
            mastery_inserts (Sequence[dict[str, Any]]): A sequence of dictionaries containing mastery level data.

        Returns:
            dict[str, Any]: The result of the insertion operation.
        """
        pass

    @abstractmethod
    def insert_equipment(
        self, equipment_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Insert equipment data into the database.

        Args:
            equipment_inserts (Sequence[dict[str, Any]]): A sequence of dictionaries containing equipment data.

        Returns:
            dict[str, Any]: The result of the insertion operation.
        """
        pass

    @abstractmethod
    def insert_skill_order(
        self, skill_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Insert skill order data into the database.

        Args:
            skill_inserts (Sequence[dict[str, Any]]): A sequence of dictionaries containing skill order data.

        Returns:
            dict[str, Any]: The result of the insertion operation.
        """
        pass

    @abstractmethod
    def insert_killed_by_data(
        self, killed_by_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Insert 'killed by' data into the database.

        Args:
            killed_by_inserts (Sequence[dict[str, Any]]): A sequence of dictionaries containing 'killed by' data.

        Returns:
            dict[str, Any]: The result of the insertion operation.
        """
        pass

    @abstractmethod
    def insert_items_purchased(
        self, item_purchases: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Insert data about items purchased into the database.

        Args:
            item_purchases (Sequence[dict[str, Any]]): A sequence of dictionaries containing item purchase data.

        Returns:
            dict[str, Any]: The result of the insertion operation.
        """
        pass

    @abstractmethod
    def insert_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """
        Insert a new user record into the database.

        Args:
            user_data (dict[str, Any]): Dictionary containing user data.

        Returns:
            dict[str, Any]: The inserted user data, potentially with additional metadata.
        """
        pass

    @abstractmethod
    def get_user_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        """
        Retrieve a user record by their nickname.

        Args:
            nickname (str): The nickname of the user to retrieve.

        Returns:
            Optional[dict[str, Any]]: The user data if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """
        Retrieve a user record by their user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[dict[str, Any]]: The user data if found, None otherwise.
        """
        pass

    @abstractmethod
    def select(
        self, table: str, columns: str = "*", **filters: Any
    ) -> Sequence[dict[str, Any]]:
        """
        Perform a select operation on the specified table with given filters.

        Args:
            table (str): The name of the table to select from.
            columns (str, optional): The columns to select. Defaults to "*".
            **filters: Arbitrary keyword arguments for filtering the selection.

        Returns:
            Sequence[dict[str, Any]]: A sequence of dictionaries containing the selected data.
        """
        pass

    @abstractmethod
    def upsert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Perform an upsert (insert or update) operation on the specified table.

        Args:
            table (str): The name of the table to upsert into.
            data (dict[str, Any]): The data to upsert.

        Returns:
            dict[str, Any]: The result of the upsert operation.
        """
        pass

    @abstractmethod
    def batch_insert(
        self, table: str, data_list: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Perform a batch insert operation on the specified table.

        Args:
            table (str): The name of the table to insert into.
            data_list (Sequence[dict[str, Any]]): A sequence of dictionaries containing the data to insert.

        Returns:
            dict[str, Any]: The result of the batch insert operation.
        """
        pass
