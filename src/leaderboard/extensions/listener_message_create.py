import aiosqlite
import hikari
import lightbulb

from leaderboard.utils import database

loader = lightbulb.Loader()


@loader.listener(hikari.GuildMessageCreateEvent)
async def on_message(
    event: hikari.GuildMessageCreateEvent, db: aiosqlite.Connection
) -> None:
    if not event.is_human:
        return

    await database.record_message(
        db,
        event.guild_id,
        event.author_id,
        event.author.username,
        len(event.message.attachments),
    )
