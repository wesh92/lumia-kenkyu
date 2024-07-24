import redis
import redis.exceptions
import pendulum
from typing import Any, Optional, Sequence
from logging import getLogger, basicConfig, INFO, DEBUG, log

from redis.client import Redis
from data_access.dao import AbstractDAO
from CONSTS import get_secrets, DAOType, Environment


class DragonflyDBDAO(AbstractDAO):
    """
    DragonflyDB (and Redis by extension) implementation of the AbstractDAO.

    Provides methods to interact with a DragonflyDB (or Redis) database.
    """

    _logger = getLogger(__name__)
    basicConfig(level=INFO)

    def __init__(self):
        """Initialize the DragonflyDBDAO."""
        self.client: Redis
        self.env: Environment = Environment.DEV
        self.namespace: str

    def initialize(self) -> None:
        """Initialize the DragonflyDB client."""
        secrets = get_secrets(DAOType.DRAGONFLYDB, self.env)
        self.client = Redis(
            connection_pool=redis.BlockingConnectionPool(
                host=secrets["host"],
                port=secrets["port"],
                password=secrets["password"],
                protocol=3,
                decode_responses=True,
                retry_on_error=[ConnectionError, redis.exceptions.ConnectionError],
            )
        )
        self.namespace = secrets["namespace"]

    def _ping(self) -> bool:
        """Check if the client is connected to the database."""
        try:
            return self.client.ping()
        except redis.exceptions.ConnectionError:
            return False

    def _datetime_pre_processor(self, input_datetime: str | pendulum.DateTime) -> int:
        """
        Dates/DateTimes need to be integers in Redis to be able to ever do range searches.
        This function will convert the input to an integer representation of the Date and Time.
        """
        if isinstance(input_datetime, str):
            return pendulum.parse(input_datetime).int_timestamp
        return input_datetime.int_timestamp

    def _index_keyspace_builder(self, insert_type: str, pk_columns: list[Any]) -> str:
        """Build a key for indexing a record in the database."""
        pk_values_to_str = [str(pk) for pk in pk_columns]
        return f"{insert_type}:{self.namespace}:{':'.join(pk_values_to_str)}"

    def insert_game(self, game_data: dict[str, Any]):
        """Insert a new game record into the DragonflyDB database."""
        game_data.update(
            {
                "game_start_time": self._datetime_pre_processor(
                    game_data["game_start_time"]
                )
            }
        )
        self._logger.info(f"Inserting game data: {game_data}")
        index = self._index_keyspace_builder(
            "games",
            [
                game_data["server"],
                game_data["game_id"],
                game_data["game_start_time"],
                game_data["season_id"],
                game_data["match_mode"],
            ],
        )
        self._logger.info(f"Indexing game data: {index}")
        self.client.hset(
            index,
            mapping=game_data,
        )

    def game_exists(self, game_id: int) -> bool:
        """
        Check if a game with the given ID exists in the database.

        Args:
            game_id (int): The ID of the game to check.

        Returns:
            bool: True if the game exists, False otherwise.
        """
        pass

    def insert_player_stats(self, player_stats: dict[str, Any]) -> dict[str, Any]:
        """
        Insert player statistics for a game into the database.

        Args:
            player_stats (dict[str, Any]): Dictionary containing player statistics.

        Returns:
            dict[str, Any]: The inserted player statistics, potentially with additional metadata.
        """
        pass

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

    def insert_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """
        Insert a new user record into the database.

        Args:
            user_data (dict[str, Any]): Dictionary containing user data.

        Returns:
            dict[str, Any]: The inserted user data, potentially with additional metadata.
        """
        pass

    def get_user_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        """
        Retrieve a user record by their nickname.

        Args:
            nickname (str): The nickname of the user to retrieve.

        Returns:
            Optional[dict[str, Any]]: The user data if found, None otherwise.
        """
        pass

    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """
        Retrieve a user record by their user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[dict[str, Any]]: The user data if found, None otherwise.
        """
        pass

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
