from typing import Any, Optional, Sequence
from data_access.dao import AbstractDAO
from CONSTS import get_secrets, DAOType, Environment
import psycopg2


class PostgresDAO(AbstractDAO):
    """
    Postgres implementation of the AbstractDAO.
    Provides methods to interact with a Postgres database.
    """

    def __init__(self):
        """Initialize the PostgresDAO."""
        self.client: psycopg2.extensions.connection
        self.env: Environment = Environment.DEV

    def initialize(self) -> None:
        """Initialize the Supabase client."""
        secrets = get_secrets(DAOType.POSTGRES, self.env)
        self.client = psycopg2.connect(
            dbname=secrets["db"],
            user=secrets["user"],
            password=secrets["password"],
            host=secrets["host"],
            port=secrets["port"],
            options=f"-c search_path={secrets['schema']}",
        )

    def insert_game(self, game_data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new game record into the Postgres database.

        Input is from `processors.prepare_processors._prepare_game_insert`.

        Input Shape:
            {
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

        Args:
            game_data (dict[str, Any]): Data to insert into the games table.

        Returns:
            dict[str, Any]: The game_id of the inserted game.

        Raises:
            psycopg2.Error: If there is an error inserting the game data.
        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                        INSERT INTO games (
                            game_id,
                            game_start_time,
                            season_id,
                            match_mode,
                            match_team_mode,
                            server,
                            duration,
                            total_match_players,
                            main_weather_code,
                            sub_weather_code
                        )
                        VALUES (
                            %(game_id)s,
                            %(game_start_time)s,
                            %(season_id)s,
                            %(match_mode)s,
                            %(match_team_mode)s,
                            %(server)s,
                            %(duration)s,
                            %(total_match_players)s,
                            %(main_weather_code)s,
                            %(sub_weather_code)s
                        )
                        ON CONFLICT (game_id) DO UPDATE SET
                            game_start_time = EXCLUDED.game_start_time,
                            season_id = EXCLUDED.season_id,
                            match_mode = EXCLUDED.match_mode,
                            match_team_mode = EXCLUDED.match_team_mode,
                            server = EXCLUDED.server,
                            duration = EXCLUDED.duration,
                            total_match_players = EXCLUDED.total_match_players,
                            main_weather_code = EXCLUDED.main_weather_code,
                            sub_weather_code = EXCLUDED.sub_weather_code
                        RETURNING *;
                        """,
                game_data,
            )
            return cursor.fetchone()

    def game_exists(self, game_id: int) -> bool:
        """Check if a game with the given ID exists in the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT game_id
                FROM games
                WHERE game_id = %(game_id)s;
                """,
                {"game_id": game_id},
            )
            return bool(cursor.fetchone())

    def insert_player_stats(self, player_stats: dict[str, Any]) -> dict[str, Any]:
        """Insert player statistics for a game into the Postgres database.

        Input is from `processors.prepare_processros._prepare_player_stats`.
        Input Shape:
            {
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

        Args:
            player_stats (dict[str, Any]): Player statistics for a game.

        Returns:
            dict[str, Any]: The game ID of the inserted record.

        Raises:
            Exception: If the game ID does not exist in the database.

        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                        INSERT INTO player_game_stats (
                            game_id,
                            game_start_time,
                            user_id,
                            nickname,
                            character_id,
                            team_id,
                            game_place_result,
                            level,
                            kills,
                            assists,
                            monster_kills,
                            damage_to_player,
                            damage_to_monster,
                            tanked_damage,
                            healing,
                            victory,
                            mmr_change,
                            mmr_before,
                            mmr_gain,
                            mmr_after,
                            starting_area,
                            deaths,
                            double_kills,
                            triple_kills,
                            quadra_kills,
                            extra_kills,
                            possessed_credits,
                            used_credits
                        )
                        VALUES (
                            %(game_id)s,
                            %(game_start_time)s,
                            %(user_id)s,
                            %(nickname)s,
                            %(character_id)s,
                            %(team_id)s,
                            %(game_place_result)s,
                            %(level)s,
                            %(kills)s,
                            %(assists)s,
                            %(monster_kills)s,
                            %(damage_to_player)s,
                            %(damage_to_monster)s,
                            %(tanked_damage)s,
                            %(healing)s,
                            %(victory)s,
                            %(mmr_change)s,
                            %(mmr_before)s,
                            %(mmr_gain)s,
                            %(mmr_after)s,
                            %(starting_area)s,
                            %(deaths)s,
                            %(double_kills)s,
                            %(triple_kills)s,
                            %(quadra_kills)s,
                            %(extra_kills)s,
                            %(possessed_credits)s,
                            %(used_credits)s
                        )
                        ON CONFLICT (game_id, user_id) DO UPDATE SET
                            game_start_time = EXCLUDED.game_start_time,
                            nickname = EXCLUDED.nickname,
                            character_id = EXCLUDED.character_id,
                            team_id = EXCLUDED.team_id,
                            game_place_result = EXCLUDED.game_place_result,
                            level = EXCLUDED.level,
                            kills = EXCLUDED.kills,
                            assists = EXCLUDED.assists,
                            monster_kills = EXCLUDED.monster_kills,
                            damage_to_player = EXCLUDED.damage_to_player,
                            damage_to_monster = EXCLUDED.damage_to_monster,
                            tanked_damage = EXCLUDED.tanked_damage,
                            healing = EXCLUDED.healing,
                            victory = EXCLUDED.victory,
                            mmr_change = EXCLUDED.mmr_change,
                            mmr_before = EXCLUDED.mmr_before,
                            mmr_gain = EXCLUDED.mmr_gain,
                            mmr_after = EXCLUDED.mmr_after,
                            starting_area = EXCLUDED.starting_area,
                            deaths = EXCLUDED.deaths,
                            double_kills = EXCLUDED.double_kills,
                            triple_kills = EXCLUDED.triple_kills,
                            quadra_kills = EXCLUDED.quadra_kills,
                            extra_kills = EXCLUDED.extra_kills,
                            possessed_credits = EXCLUDED.possessed_credits,
                            used_credits = EXCLUDED.used_credits
                        RETURNING *;
                        """,
                player_stats,
            )
            return cursor.fetchone()

    def player_game_stats_exist(self, game_id: int, user_id: int) -> bool:
        """Check if player statistics exist for a given game and user in the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT game_id
                FROM player_game_stats
                WHERE game_id = %(game_id)s
                AND user_id = %(user_id)s;
                """,
                {"game_id": game_id, "user_id": user_id},
            )
            return bool(cursor.fetchone())

    def insert_mastery_levels(
        self, mastery_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert mastery levels data into the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO mastery_levels (
                    game_start_time,
                    game_id,
                    user_id,
                    mastery_type,
                    level
                )
                VALUES (
                    %(game_start_time)s,
                    %(game_id)s,
                    %(user_id)s,
                    %(mastery_type)s,
                    %(level)s
                )
                ON CONFLICT (game_start_time, game_id, user_id, mastery_type)
                DO UPDATE SET
                game_start_time = EXCLUDED.game_start_time,
                game_id = EXCLUDED.game_id,
                user_id = EXCLUDED.user_id,
                mastery_type = EXCLUDED.mastery_type,
                level = EXCLUDED.level
                RETURNING game_id;
                """,
                mastery_inserts,
            )
            return {"game_id": cursor.fetchone()[0]}

    def insert_equipment(
        self, equipment_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert equipment data into the Postgres database.

        Input is from `processors.prepare_processors._prepare_equipment_inserts

        Input Shape:
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "slot": int(slot),
                "item_id": item_id,
                "type": 2,  # Final equipment, 1 for starting equipment
            }

        Args:
            equipment_inserts (Sequence[dict[str, Any]]): Equipment data to insert into the database.

        Returns:
            dict[str, Any]: The game ID of the inserted record.


        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO equipment (
                    game_start_time,
                    game_id,
                    user_id,
                    slot,
                    item_id,
                    type
                )
                VALUES (
                    %(game_start_time)s,
                    %(game_id)s,
                    %(user_id)s,
                    %(slot)s,
                    %(item_id)s,
                    %(type)s
                )
                ON CONFLICT (game_start_time, game_id, user_id, slot)
                DO UPDATE SET
                game_start_time = EXCLUDED.game_start_time,
                game_id = EXCLUDED.game_id,
                user_id = EXCLUDED.user_id,
                slot = EXCLUDED.slot,
                item_id = EXCLUDED.item_id,
                type = EXCLUDED.type
                RETURNING game_id;
                """,
                equipment_inserts,
            )
            return {"game_id": cursor.fetchone()[0]}

    def insert_skill_order(
        self, skill_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert skill order data into the Postgres database.

        Input is from `processors.prepare_processors._prepare_skill_inserts`

        Input Shape:
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "skill_level": int(skill_level),
                "skill_id": skill_id,
            }

        Args:
            skill_inserts (Sequence[dict[str, Any]]): Skill order data to insert into the database.

        Returns:
            dict[str, Any]: The game ID of the inserted record.
        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO skill_order (
                    game_start_time,
                    game_id,
                    user_id,
                    skill_level,
                    skill_id
                )
                VALUES (
                    %(game_start_time)s,
                    %(game_id)s,
                    %(user_id)s,
                    %(skill_level)s,
                    %(skill_id)s
                )
                ON CONFLICT (game_start_time, game_id, user_id, skill_level)
                DO UPDATE SET
                game_start_time = EXCLUDED.game_start_time,
                game_id = EXCLUDED.game_id,
                user_id = EXCLUDED.user_id,
                skill_level = EXCLUDED.skill_level,
                skill_id = EXCLUDED.skill_id
                RETURNING game_id;
                """,
                skill_inserts,
            )
            return {"game_id": cursor.fetchone()[0]}

    def insert_killed_by_data(
        self, killed_by_inserts: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert 'killed by' data into the Postgres database.

        Input is from `processors.prepare_processors._prepare_killed_by_inserts`

        Input Shape:
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

        Args:
            killed_by_inserts (Sequence[dict[str, Any]]): 'Killed by' data to insert into the database.

        Returns:
            dict[str, Any]: The game ID of the inserted record.
        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO killed_by_data (
                    game_start_time,
                    game_id,
                    user_id,
                    killed_by_id,
                    killed_by_type,
                    killed_by_name,
                    died_area,
                    killed_by_character,
                    killed_by_character_weapon
                )
                VALUES (
                    %(game_start_time)s,
                    %(game_id)s,
                    %(user_id)s,
                    %(killed_by_id)s,
                    %(killed_by_type)s,
                    %(killed_by_name)s,
                    %(died_area)s,
                    %(killed_by_character)s,
                    %(killed_by_character_weapon)s
                )
                ON CONFLICT (game_start_time, game_id, user_id, killed_by_id)
                DO UPDATE SET
                game_start_time = EXCLUDED.game_start_time,
                game_id = EXCLUDED.game_id,
                user_id = EXCLUDED.user_id,
                killed_by_id = EXCLUDED
                RETURNING game_id;
                """,
                killed_by_inserts,
            )
            return {"game_id": cursor.fetchone()[0]}

    def insert_items_purchased(
        self, item_purchases: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Insert data about items purchased into the Postgres database.

        Input is from `processors.prepare_processors._prepare_item_purchases`

        Input Shape:
            {
                "game_start_time": game_data.game_start_datetime.isoformat(),
                "game_id": game_data.game_id,
                "user_id": game_data.user_id,
                "item_id": item_id,
                "purchase_type": "console", # Or "drone"
                "quantity": quantity,
            }

        Args:
            item_purchases (Sequence[dict[str, Any]]): Item purchase data to insert into the database.

        Returns:
            dict[str, Any]: The game ID of the inserted record."""

        with self.client.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO items_purchased (
                    game_start_time,
                    game_id,
                    user_id,
                    item_id,
                    purchase_type,
                    quantity
                )
                VALUES (
                    %(game_start_time)s,
                    %(game_id)s,
                    %(user_id)s,
                    %(item_id)s,
                    %(purchase_type)s,
                    %(quantity)s
                )
                ON CONFLICT (game_start_time, game_id, user_id, item_id, purchase_type)
                DO UPDATE SET
                game_start_time = EXCLUDED.game_start_time,
                game_id = EXCLUDED.game_id,
                user_id = EXCLUDED.user_id,
                item_id = EXCLUDED.item_id,
                purchase_type = EXCLUDED.purchase_type,
                quantity = EXCLUDED.quantity
                RETURNING game_id;
                """,
                item_purchases,
            )
            return {"game_id": cursor.fetchone()[0]}

    def insert_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new user record into the Postgres database.

        Input is directly from `game_data_cli`

        Input Shape: {"user_id": user.user_id, "nickname": user.nickname}

        Args:
            user_data (dict[str, Any]): User data to insert into the database.

        Returns:
            dict[str, Any]: The user ID of the inserted record.
        """
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                        INSERT INTO users (
                            user_id,
                            nickname
                        )
                        VALUES (
                            %(user_id)s,
                            %(nickname)s
                        )
                        ON CONFLICT (user_id) DO UPDATE SET
                            nickname = EXCLUDED.nickname
                        RETURNING *;
                        """,
                user_data,
            )
            return cursor.fetchone()

    def get_user_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        """Retrieve a user record by their nickname from the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM users
                WHERE nickname = %(nickname)s;
                """,
                {"nickname": nickname},
            )
            return cursor.fetchone()

    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a user record by their user ID from the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM users
                WHERE user_id = %(user_id)s;
                """,
                {"user_id": user_id},
            )
            return cursor.fetchone()

    def select(
        self, table: str, columns: str = "*", **filters: Any
    ) -> Sequence[dict[str, Any]]:
        """Perform a select operation on the specified table with given filters in the Postgres database."""
        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT {columns} FROM {table}
                WHERE {where_clause};
                """.format(
                    columns=columns,
                    table=table,
                    where_clause=" AND ".join(
                        f"{key} = %({key})s" for key in filters.keys()
                    ),
                ),
                filters,
            )
            return cursor.fetchall()

    def upsert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Perform an upsert operation on the specified table in the Postgres database."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"%({key})s" for key in data.keys())
        update_set = ", ".join(f"{key} = EXCLUDED.{key}" for key in data.keys())

        with self.client.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
                ON CONFLICT DO UPDATE SET
                {update_set}
                RETURNING *;
                """,
                data,
            )
            return cursor.fetchone()

    def batch_insert(
        self, table: str, data_list: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Perform a batch insert operation on the specified table in the Postgres database."""
        if not data_list:
            return []

        columns = ", ".join(data_list[0].keys())
        placeholders = ", ".join(f"%({key})s" for key in data_list[0].keys())
        update_set = ", ".join(f"{key} = EXCLUDED.{key}" for key in data_list[0].keys())

        with self.client.cursor() as cursor:
            cursor.executemany(
                f"""
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
                ON CONFLICT DO UPDATE SET
                {update_set}
                RETURNING *;
                """,
                data_list,
            )
            return cursor.fetchall()
