import aiosqlite
import hikari
import lightbulb

from leaderboard import config
from leaderboard.utils import database

loader = lightbulb.Loader()


@loader.command
class LeaderboardCommand(
    lightbulb.SlashCommand,
    name="leaderboard",
    description="Displays the guild's top 10 users by recorded message and attachment counts.",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, db: aiosqlite.Connection) -> None:
        guild_id = ctx.guild_id
        if not guild_id:
            await ctx.respond("Sorry, this command can only be used in a guild.")
            return

        message_leaders, attachment_leaders = await database.get_leaderboard_for_guild(
            db, guild_id
        )

        container = hikari.impl.ContainerComponentBuilder(
            accent_color=config.DEFAULT_COLOUR
        )

        container.add_text_display("## Message Count Leaderboard")
        if not message_leaders:
            container.add_text_display("No messages recorded yet.")

        for rank, row in enumerate(message_leaders, start=1):
            container.add_text_display(
                f"{rank}. {row['user_username']} - {row['message_count']}"
            )

        container.add_separator(divider=True)

        container.add_text_display("## Message Attachment Count Leaderboard")
        if not attachment_leaders:
            container.add_text_display("No attachments recorded yet.")

        for rank, row in enumerate(attachment_leaders, start=1):
            container.add_text_display(
                f"{rank}. {row['user_username']} - {row['attachment_count']}"
            )

        await ctx.respond(components=[container])
