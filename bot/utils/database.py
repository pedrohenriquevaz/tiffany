"""
Utilitários para gerenciar dados do bot
"""
from typing import Dict, Any, Optional
from datetime import datetime

class GuildSettings:
    """Gerencia configurações de um servidor Discord"""
    
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.settings = {
            'battle_channel': None,
            'prize_pool_text': 'Uma premiação misteriosa',
            'battle_timeout': 60,  # segundos
            'timeout_message': 'Um dos usuários não aceitou o desafio a tempo.',
            'battle_message': 'Que comece o duelo!',
            'last_bump': None,
        }
    
    def set(self, key: str, value: Any) -> None:
        """Define um valor de configuração"""
        self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor de configuração"""
        return self.settings.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna um dicionário com todas as configurações"""
        return self.settings.copy()


class SettingsManager:
    """Gerencia as configurações de todos os servidores"""
    
    def __init__(self):
        self.guilds: Dict[int, GuildSettings] = {}
    
    def get_guild_settings(self, guild_id: int) -> GuildSettings:
        """Obtém ou cria as configurações de um servidor"""
        if guild_id not in self.guilds:
            self.guilds[guild_id] = GuildSettings(guild_id)
        return self.guilds[guild_id]
    
    def get_all_guilds(self) -> Dict[int, GuildSettings]:
        """Retorna todas as configurações de servidores"""
        return self.guilds.copy()


# Instância global do gerenciador de configurações
settings_manager = SettingsManager()
