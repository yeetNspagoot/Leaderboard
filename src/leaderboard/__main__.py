import aiosqlite
import hikari
import lightbulb

from leaderboard import config, extensions
from leaderboard.utils import database


def main() -> None:
    bot = hikari.GatewayBot(
        token=config.DISCORD_TOKEN,
        intents=hikari.Intents.GUILDS
        | hikari.Intents.GUILD_MESSAGES
        | hikari.Intents.MESSAGE_CONTENT,
    )

    client = lightbulb.client_from_app(bot)

    @bot.listen(hikari.StartingEvent)
    async def on_starting(_: hikari.StartingEvent) -> None:

        client.di.registry_for(lightbulb.di.Contexts.DEFAULT).register_factory(
            aiosqlite.Connection,
            database.open_database,
            teardown=aiosqlite.Connection.close,
        )

        await client.load_extensions_from_package(extensions, recursive=True)
        await client.start()

    @bot.listen(hikari.StoppingEvent)
    async def on_stopping(_: hikari.StoppingEvent) -> None:
        await client.stop()

    bot.run()


if __name__ == "__main__":
    main()
