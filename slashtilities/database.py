import asyncio
import os
from typing import Dict

import asyncpg
from discord import User


class Database:
    def __init__(self) -> None:
        self.stmts: Dict[str, asyncpg.prepared_stmt.PreparedStatement] = {}
        self.DEFAULTS = {"should_dm": True}

        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(os.environ["DATABASE_URL"])
        )
        loop.run_until_complete(self._init_db())

    async def _init_db(self) -> None:
        async with self.pool.acquire() as conn:
            try:
                async with conn.transaction():
                    await conn.execute(
                        "CREATE TABLE slashtilities "
                        "(snowflake BIGINT NOT NULL PRIMARY KEY, should_dm boolean);"
                    )
            except asyncpg.exceptions.DuplicateTableError:
                pass
        await self._prepare_db_stmts()

    async def _prepare_db_stmts(self) -> None:
        # ...because *actually* preparing statements is complex
        self.stmts["get_pref"] = "SELECT * FROM slashtilities WHERE snowflake=$1"

    async def get_preferences_for(self, user: int) -> Dict[str, asyncpg.Record]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return {
                    k: v
                    for record in await conn.fetch(self.stmts["get_pref"], user)
                    for k, v in record.items()
                } or self.DEFAULTS

    async def update_preferences_for(self, user: int, to: bool) -> None:
        async with self.pool.acquire() as conn:
            try:
                async with conn.transaction():
                    await conn.execute(
                        "INSERT INTO slashtilities (snowflake, should_dm) VALUES ($1, $2)",
                        user,
                        to,
                    )
            except asyncpg.exceptions.UniqueViolationError:
                pass
            async with conn.transaction():
                await conn.execute(
                    "UPDATE slashtilities SET should_dm=$2 WHERE snowflake=$1",
                    user,
                    to,
                )

            # Space optimization
            if await self.get_preferences_for(user) == self.DEFAULTS:
                async with conn.transaction():
                    await conn.execute(
                        "DELETE FROM slashtilities WHERE snowflake=$1", user
                    )

    async def should_dm(self, user: User) -> bool:
        return (await self.get_preferences_for(user.id)).get("should_dm", True)

    # async def add(self, user: int) -> None:
    #     async with self.pool.acquire() as conn:
    #         async with conn.transaction():
    #             await conn.execute(
    #                 "INSERT INTO slashtilities (snowflake, should_dm) VALUES ($1, TRUE)",
    #                 user,
    #             )
