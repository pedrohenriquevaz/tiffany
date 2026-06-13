import os
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# Bump command configuration
BUMP_COOLDOWN_HOURS = 2

# Battle configuration
TIER_ROLES = {
    '🎴ㅤÉpico': 'epic',
    '🀄ㅤLenda': 'legend',
    '🌗ㅤMítico': 'mythic',
    '🌗ㅤHonra': 'honor',
    '🌓ㅤGlória': 'glory',
    '🌒ㅤImortal': 'immortal',
}

# Guild settings storage (será usado para armazenar configurações por servidor)
GUILD_SETTINGS = {}
