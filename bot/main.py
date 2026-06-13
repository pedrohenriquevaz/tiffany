"""
Bot Principal - Sunflower Discord Bot
"""
import discord
from discord.ext import commands
import os
from config import DISCORD_TOKEN, GUILD_ID


# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

# Criação do bot
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None,
    application_id=None
)


@bot.event
async def on_ready():
    """Executado quando o bot está pronto"""
    print(f'Bot {bot.user} está online!')
    try:
        # Sincronizar slash commands
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} slash commands')
    except Exception as e:
        print(f'Erro ao sincronizar slash commands: {e}')


async def load_cogs():
    """Carrega todos os cogs da pasta cogs"""
    cogs_dir = 'cogs'
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                print(f'✅ Cog {cog_name} carregado com sucesso!')
            except Exception as e:
                print(f'❌ Erro ao carregar cog {cog_name}: {e}')


async def main():
    """Função principal"""
    async with bot:
        # Carregar cogs
        await load_cogs()
        
        # Iniciar bot
        await bot.start(DISCORD_TOKEN)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
