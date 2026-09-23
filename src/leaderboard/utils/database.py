from pathlib import Path

import aiosqlite
import hikari

from leaderboard import config


async def open_database() -> aiosqlite.Connection:
    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    db = await aiosqlite.connect(config.DB_PATH)
    db.row_factory = aiosqlite.Row

    try:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS leaderboard (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                user_username TEXT NOT NULL,
                message_count INTEGER NOT NULL,
                attachment_count INTEGER NOT NULL,
                PRIMARY KEY (guild_id, user_id)
            );
            """
        )
        await db.commit()
    except Exception:
        await db.close()
        raise

    return db


async def record_message(
    db: aiosqlite.Connection,
    guild_id: hikari.Snowflake,
    user_id: hikari.Snowflake,
    username: str,
    attachment_count: int,
) -> None:
    await db.execute(
        """
        INSERT INTO leaderboard (
            guild_id, user_id, user_username, message_count, attachment_count
        )
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT (guild_id, user_id) DO UPDATE SET
            user_username = excluded.user_username,
            message_count = message_count + 1,
            attachment_count = attachment_count + excluded.attachment_count
        """,
        (int(guild_id), int(user_id), username, attachment_count),
    )
    await db.commit()


async def get_leaderboard_for_guild(
    db: aiosqlite.Connection, guild_id: hikari.Snowflake
) -> tuple[list[aiosqlite.Row], list[aiosqlite.Row]]:
    LIMIT = 10

    async with db.execute(
        """
        SELECT user_id, user_username, message_count, attachment_count
        FROM leaderboard
        WHERE guild_id = ?
        ORDER BY message_count DESC, user_id ASC
        LIMIT ?
        """,
        (int(guild_id), LIMIT),
    ) as cursor:
        message_leaders = list(await cursor.fetchall())

    async with db.execute(
        """
        SELECT user_id, user_username, message_count, attachment_count
        FROM leaderboard
        WHERE guild_id = ? AND attachment_count > 0
        ORDER BY attachment_count DESC, user_id ASC
        LIMIT ?
        """,
        (int(guild_id), LIMIT),
    ) as cursor:
        attachment_leaders = list(await cursor.fetchall())

    return message_leaders, attachment_leaders
