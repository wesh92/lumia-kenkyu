import redis
import redis.exceptions
from typing import Any, Optional, Sequence

from redis.client import Redis
from data_access.dao import AbstractDAO
from CONSTS import get_secrets, DAOType, Environment


class DragonflyDBDAO(AbstractDAO):
    """
    DragonflyDB (and Redis by extension) implementation of the AbstractDAO.

    Provides methods to interact with a DragonflyDB (or Redis) database.
    """

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
