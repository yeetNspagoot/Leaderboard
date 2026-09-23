# Leaderboard
A Discord bot that tracks message and attachment counts and displays per-guild leaderboards.

## Invite
[Add Leaderboard to your guild](https://discord.com/oauth2/authorize?client_id=1552225429103054948)

Use `/leaderboard` to see your server's top 10 users by messages and attachments.

## How it works
- **Only counts new messages and attachments sent after the bot is added and while it is online.** 
  - (Earlier messages and activity while the bot is offline are not counted.)
- Ignores bots and webhooks.
- Keeps separate totals for each server.
- Saves counts between restarts.
- Does not import history or subtract deleted messages.

The bot needs **View Channels** permission in the channels you want counted.

## Self-hosting
Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

1. Clone this repository.
2. Copy `.env.example` to `.env` and set `DISCORD_TOKEN`.
3. Enable **Message Content Intent** in the Discord Developer Portal.
4. Install your bot with the `bot` and `applications.commands` scopes.
5. Run from the project directory:

   ```sh
   uv sync
   uv run leaderboard
   ```

## License
[MIT](LICENSE)

*This README was written with AI assistance.*
