import os
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))
COMMAND_PREFIX = '!'
