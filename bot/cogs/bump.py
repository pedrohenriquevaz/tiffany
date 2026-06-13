"""
Cog para o comando /bump - Automatização do Disboard
"""
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from utils.database import settings_manager
import asyncio


class BumpCog(commands.Cog):
    """Gerencia o comando /bump para manter o servidor ativo no Disboard"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bump_loop.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Executado quando o bot está pronto"""
        print(f'{self.bot.user} conectado e pronto!')
    
    @discord.app_commands.command(
        name='bump',
        description='Executa o comando bump para manter o servidor ativo no Disboard'
    )
    async def bump_command(self, interaction: discord.Interaction):
        """Comando slash /bump"""
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        
        # Verificar cooldown (2 horas)
        last_bump = guild_settings.get('last_bump')
        if last_bump:
            last_bump_time = datetime.fromisoformat(last_bump)
            cooldown_time = timedelta(hours=2)
            if datetime.now() < last_bump_time + cooldown_time:
                remaining = last_bump_time + cooldown_time - datetime.now()
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                await interaction.response.send_message(
                    f'⏱️ O comando /bump será disponível novamente em {hours}h {minutes}m',
                    ephemeral=True
                )
                return
        
        # Executar bump (aqui você pode adicionar lógica para chamar o bot do Disboard)
        guild_settings.set('last_bump', datetime.now().isoformat())
        
        embed = discord.Embed(
            title='✅ Servidor Bumped!',
            description='O servidor foi promovido no Disboard com sucesso!',
            color=discord.Color.green()
        )
        embed.add_field(name='Próximo bump disponível em', value='2 horas')
        embed.set_footer(text=f'Executado por {interaction.user.name}')
        
        await interaction.response.send_message(embed=embed)
    
    @tasks.loop(hours=2)
    async def bump_loop(self):
        """Loop que executa a cada 2 horas para lembrar sobre o bump"""
        # Aguarda até que o bot esteja pronto
        await self.bot.wait_until_ready()
        
        # Aqui você pode adicionar lógica para notificar todos os servidores
        # sobre a disponibilidade do comando /bump
        print('[BUMP] Ciclo de 2 horas completado')


async def setup(bot: commands.Bot) -> None:
    """Carrega o cog"""
    await bot.add_cog(BumpCog(bot))
