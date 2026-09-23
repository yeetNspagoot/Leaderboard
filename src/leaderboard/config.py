import os

import hikari
from dotenv import load_dotenv

load_dotenv()

# Environment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
if not DISCORD_TOKEN or DISCORD_TOKEN == "your_token_here":
    raise RuntimeError(
        "Set DISCORD_TOKEN in your environment or .env file before starting the bot."
    )

# Bot
DEFAULT_COLOUR = hikari.Colour(0x514C70)

# Paths
DB_PATH = "data/leaderboard.db"
