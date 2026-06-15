"""
Cog para o comando /battle - Duelos entre usuários
"""
import discord
from discord.ext import commands
from typing import Optional, List
import random
import asyncio
from utils.database import settings_manager
from config import TIER_ROLES


class BattleCog(commands.Cog):
    """Gerencia o sistema de duelos entre usuários"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_battles = {}  # guild_id -> battle_data
    
    @discord.app_commands.command(
        name='battle',
        description='Sorteia 2 usuários para um duelo'
    )
    async def battle_command(self, interaction: discord.Interaction):
        """Comando /battle - Inicia um novo duelo"""
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        battle_channel = guild_settings.get('battle_channel')
        
        if not battle_channel:
            await interaction.response.send_message(
                '❌ Canal de duelo não configurado! Use /battleChat para configurar.',
                ephemeral=True
            )
            return
        
        # Obter usuários ativos do dia
        active_users = await self._get_active_users(interaction.guild)
        
        if len(active_users) < 2:
            await interaction.response.send_message(
                '❌ Não há usuários suficientes ativos para um duelo.',
                ephemeral=True
            )
            return
        
        # Agrupar usuários por tier
        users_by_tier = await self._group_users_by_tier(active_users)
        
        if not users_by_tier:
            await interaction.response.send_message(
                '❌ Nenhum usuário com cargos de tier encontrado.',
                ephemeral=True
            )
            return
        
        # Selecionar um tier aleatoriamente
        selected_tier = random.choice(list(users_by_tier.keys()))
        tier_users = users_by_tier[selected_tier]
        
        if len(tier_users) < 2:
            await interaction.response.send_message(
                f'❌ Menos de 2 usuários com o tier "{selected_tier}" estão ativos.',
                ephemeral=True
            )
            return
        
        # Selecionar 2 usuários aleatórios
        champion1, champion2 = random.sample(tier_users, 2)
        
        # Obter o canal de duelo
        try:
            channel = interaction.guild.get_channel(int(battle_channel))
            if not channel:
                raise ValueError('Canal não encontrado')
        except (ValueError, TypeError):
            await interaction.response.send_message(
                '❌ Canal de duelo configurado inválido.',
                ephemeral=True
            )
            return
        
        # Criar mensagem de duelo
        prize_pool = guild_settings.get('prize_pool_text', 'Uma premiação misteriosa')
        timeout = guild_settings.get('battle_timeout', 60)
        
        embed = discord.Embed(
            title='⚔️ DESAFIO ACEITO!',
            description=f'{champion1.mention} vs {champion2.mention}',
            color=discord.Color.gold()
        )
        embed.add_field(name='Tier', value=selected_tier, inline=False)
        embed.add_field(name='Prêmio', value=prize_pool, inline=False)
        embed.add_field(
            name='Como participar',
            value=f'Reaja com ✅ para aceitar o duelo!\nTempo limite: {timeout}s',
            inline=False
        )
        
        # Enviar mensagem
        battle_message = await channel.send(
            f'{champion1.mention} {champion2.mention}',
            embed=embed
        )
        
        # Adicionar reações
        await battle_message.add_reaction('✅')
        await battle_message.add_reaction('❌')
        
        # Armazenar dados do duelo
        self.active_battles[interaction.guild.id] = {
            'message_id': battle_message.id,
            'channel_id': channel.id,
            'champion1': champion1.id,
            'champion2': champion2.id,
            'timeout': timeout,
            'accepted': {}
        }
        
        # Responder à interação IMEDIATAMENTE (Discord timeout = 3s)
        await interaction.response.send_message(
            f'✅ Duelo iniciado! Verifique {channel.mention}',
            ephemeral=True
        )
        
        # Aguardar respostas em background (sem bloquear)
        asyncio.create_task(
            self._wait_for_confirmations(
                interaction.guild.id,
                battle_message,
                champion1,
                champion2,
                timeout
            )
        )
    
    @discord.app_commands.command(
        name='prize_pool',
        description='Configura o texto de premiação para os duelos'
    )
    async def prize_pool_command(
        self,
        interaction: discord.Interaction,
        texto: str
    ):
        """Comando /prizePool - Define a premiação"""
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                '❌ Você precisa ser administrador para usar este comando.',
                ephemeral=True
            )
            return
        
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        guild_settings.set('prize_pool_text', texto)
        
        embed = discord.Embed(
            title='✅ Premiação Configurada',
            description=f'Nova premiação: {texto}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @discord.app_commands.command(
        name='battle_chat',
        description='Define o canal onde os duelos acontecerão'
    )
    @discord.app_commands.describe(
        canal='O canal onde os duelos serão postados'
    )
    async def battle_chat_command(
        self,
        interaction: discord.Interaction,
        canal: discord.TextChannel
    ):
        """Comando /battleChat - Define o canal de duelos"""
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                '❌ Você precisa ser administrador para usar este comando.',
                ephemeral=True
            )
            return
        
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        guild_settings.set('battle_channel', str(canal.id))
        
        embed = discord.Embed(
            title='✅ Canal de Duelo Configurado',
            description=f'Os duelos acontecerão em {canal.mention}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @discord.app_commands.command(
        name='set_time',
        description='Configura o tempo limite para aceitar um duelo'
    )
    async def set_time_command(
        self,
        interaction: discord.Interaction,
        segundos: int
    ):
        """Comando /setTime - Define o tempo limite para resposta"""
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                '❌ Você precisa ser administrador para usar este comando.',
                ephemeral=True
            )
            return
        
        if segundos < 10 or segundos > 600:
            await interaction.response.send_message(
                '❌ O tempo deve estar entre 10 e 600 segundos.',
                ephemeral=True
            )
            return
        
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        guild_settings.set('battle_timeout', segundos)
        
        embed = discord.Embed(
            title='✅ Tempo Configurado',
            description=f'Tempo limite para aceitar duelos: {segundos}s',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @discord.app_commands.command(
        name='message_run',
        description='Configura a mensagem quando um usuário não aceita o duelo'
    )
    async def message_run_command(
        self,
        interaction: discord.Interaction,
        mensagem: str
    ):
        """Comando /messageRun - Define mensagem de timeout"""
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                '❌ Você precisa ser administrador para usar este comando.',
                ephemeral=True
            )
            return
        
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        guild_settings.set('timeout_message', mensagem)
        
        embed = discord.Embed(
            title='✅ Mensagem Configurada',
            description=f'Nova mensagem: {mensagem}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @discord.app_commands.command(
        name='message_battle',
        description='Configura a mensagem de início do duelo'
    )
    async def message_battle_command(
        self,
        interaction: discord.Interaction,
        mensagem: str
    ):
        """Comando /messageBattle - Define mensagem de início"""
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                '❌ Você precisa ser administrador para usar este comando.',
                ephemeral=True
            )
            return
        
        guild_settings = settings_manager.get_guild_settings(interaction.guild.id)
        guild_settings.set('battle_message', mensagem)
        
        embed = discord.Embed(
            title='✅ Mensagem Configurada',
            description=f'Nova mensagem: {mensagem}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    async def _get_active_users(self, guild: discord.Guild) -> List[discord.Member]:
        """Obtém usuários que foram ativos no dia (mensagem ou call)"""
        active_users = []
        # Esta é uma implementação simplificada
        # Em produção, você precisaria rastrear atividades em um banco de dados
        
        for member in guild.members:
            if not member.bot:
                active_users.append(member)
        
        return active_users
    
    async def _group_users_by_tier(
        self,
        users: List[discord.Member]
    ) -> dict:
        """Agrupa usuários por tier baseado em roles"""
        users_by_tier = {}
        
        for user in users:
            for role in user.roles:
                if role.name in TIER_ROLES:
                    tier_name = role.name
                    if tier_name not in users_by_tier:
                        users_by_tier[tier_name] = []
                    users_by_tier[tier_name].append(user)
                    break
        
        return users_by_tier
    
    async def _wait_for_confirmations(
        self,
        guild_id: int,
        message: discord.Message,
        champion1: discord.Member,
        champion2: discord.Member,
        timeout: int
    ):
        """Aguarda as confirmações dos campeões"""
        
        def check_reaction(reaction, user):
            return (
                user in [champion1, champion2] and
                reaction.message.id == message.id and
                str(reaction.emoji) in ['✅', '❌']
            )
        
        try:
            # Aguardar até 2 reações (uma de cada jogador)
            while True:
                reaction, user = await self.bot.wait_for(
                    'reaction_add',
                    check=check_reaction,
                    timeout=timeout
                )
                
                battle_data = self.active_battles.get(guild_id)
                if not battle_data:
                    return
                
                if str(reaction.emoji) == '✅':
                    user_id = user.id
                    battle_data['accepted'][user_id] = True
                    
                    # Se ambos aceitaram
                    if (
                        battle_data['champion1'] in battle_data['accepted'] and
                        battle_data['champion2'] in battle_data['accepted']
                    ):
                        guild_settings = settings_manager.get_guild_settings(guild_id)
                        battle_msg = guild_settings.get('battle_message', 'Que comece o duelo!')
                        
                        embed = discord.Embed(
                            title='⚔️ DUELO INICIADO!',
                            description=battle_msg,
                            color=discord.Color.red()
                        )
                        await message.reply(embed=embed)
                        del self.active_battles[guild_id]
                        return
                        
                elif str(reaction.emoji) == '❌':
                    # Um usuário recusou
                    guild_settings = settings_manager.get_guild_settings(guild_id)
                    timeout_msg = guild_settings.get('timeout_message')
                    
                    embed = discord.Embed(
                        title='❌ Duelo Cancelado',
                        description=timeout_msg,
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed)
                    del self.active_battles[guild_id]
                    return
        
        except asyncio.TimeoutError:
            # Timeout
            guild_settings = settings_manager.get_guild_settings(guild_id)
            timeout_msg = guild_settings.get('timeout_message')
            
            embed = discord.Embed(
                title='⏱️ Tempo Expirado',
                description=timeout_msg,
                color=discord.Color.orange()
            )
            await message.reply(embed=embed)
            del self.active_battles[guild_id]


async def setup(bot: commands.Bot) -> None:
    """Carrega o cog"""
    await bot.add_cog(BattleCog(bot))
