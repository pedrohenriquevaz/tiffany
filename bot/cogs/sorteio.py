"""
Cog de Sorteio - Sorteia membros ativos para realizar atividades
"""
import discord
from discord.ext import commands
from discord import app_commands
import random


# Lista de GIFs de celebração/sorteio
GIFS_SORTEIO = [
    "https://media.giphy.com/media/3o6ZtpWzQAF8ZZV9A4/giphy.gif",
    "https://media.giphy.com/media/l3q2K5jinAlZ0OWDi/giphy.gif",
    "https://media.giphy.com/media/3o7TKcqMJuCBp6m3dq/giphy.gif",
    "https://media.giphy.com/media/l0HlTy9x8FZo0XO1i/giphy.gif",
    "https://media.giphy.com/media/k2QJ4eYSvVABkpXr0l/giphy.gif",
    "https://media.giphy.com/media/l0HkDtMQqF6nB1LwA/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
]


class Sorteio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='sorteio', description='Sorteia um membro ativo para realizar uma atividade')
    @app_commands.describe(
        atividade='A atividade que será realizada',
        com_gif='Enviar um GIF aleatório com a mensagem? (padrão: Sim)'
    )
    async def sorteio(
        self, 
        interaction: discord.Interaction, 
        atividade: str,
        com_gif: bool = True
    ):
        """
        Sorteia um membro ativo do servidor para realizar uma atividade
        
        Args:
            interaction: Interação do Discord
            atividade: A atividade a ser realizada
            com_gif: Se deve enviar um GIF aleatório (True/False)
        """
        try:
            # Obtém o guild (servidor)
            guild = interaction.guild
            if not guild:
                await interaction.response.send_message(
                    "❌ Este comando só funciona em servidores!",
                    ephemeral=True
                )
                return
            
            # Filtra membros ativos (excluindo bots e o próprio bot)
            membros_ativos = [
                membro for membro in guild.members 
                if not membro.bot and membro.status != discord.Status.offline
            ]
            
            if not membros_ativos:
                await interaction.response.send_message(
                    "❌ Nenhum membro ativo encontrado no servidor!",
                    ephemeral=True
                )
                return
            
            # Sorteia um membro
            sorteado = random.choice(membros_ativos)
            
            # Cria a mensagem
            mensagem = f"🎲 O usuário {sorteado.mention} foi sorteado para **{atividade}**!"
            
            # Cria embed com GIF se solicitado
            if com_gif:
                gif_url = random.choice(GIFS_SORTEIO)
                embed = discord.Embed(
                    description=mensagem,
                    color=discord.Color.gold()
                )
                embed.set_image(url=gif_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(mensagem)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao realizar sorteio: {str(e)}",
                ephemeral=True
            )


async def setup(bot):
    """Carrega o cog no bot"""
    await bot.add_cog(Sorteio(bot))
