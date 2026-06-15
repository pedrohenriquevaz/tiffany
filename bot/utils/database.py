"""
Gerenciador de configurações usando JSON
"""
import json
import os
from pathlib import Path
from threading import Lock
from typing import Dict, Any


class SettingsManager:
    """Gerencia configurações do servidor armazenadas em JSON"""
    
    def __init__(self, filepath: str = 'data/guild_settings.json'):
        """
        Inicializa o gerenciador de configurações
        
        Args:
            filepath: Caminho do arquivo JSON para armazenar as configurações
        """
        self.filepath = filepath
        self.lock = Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Cria o arquivo JSON se não existir"""
        Path(self.filepath).parent.mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega todos os dados do arquivo JSON"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """Salva dados no arquivo JSON"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_guild_settings(self, guild_id: int) -> 'GuildSettings':
        """
        Obtém as configurações de um servidor
        
        Args:
            guild_id: ID do servidor Discord
            
        Returns:
            GuildSettings: Objeto com as configurações do servidor
        """
        with self.lock:
            data = self._load_data()
            guild_str = str(guild_id)
            
            if guild_str not in data:
                data[guild_str] = {}
                self._save_data(data)
            
            return GuildSettings(self, guild_id, data[guild_str])
    
    def save_guild_settings(self, guild_id: int, settings: Dict[str, Any]) -> None:
        """
        Salva as configurações de um servidor
        
        Args:
            guild_id: ID do servidor Discord
            settings: Dicionário com as configurações
        """
        with self.lock:
            data = self._load_data()
            data[str(guild_id)] = settings
            self._save_data(data)


class GuildSettings:
    """Representa as configurações de um servidor específico"""
    
    def __init__(self, manager: SettingsManager, guild_id: int, data: Dict[str, Any]):
        """
        Inicializa as configurações do servidor
        
        Args:
            manager: SettingsManager para salvar alterações
            guild_id: ID do servidor Discord
            data: Dicionário com os dados atuais
        """
        self.manager = manager
        self.guild_id = guild_id
        self.data = data.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém uma configuração
        
        Args:
            key: Chave da configuração
            default: Valor padrão se a chave não existir
            
        Returns:
            Valor da configuração ou default
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Define uma configuração e a salva
        
        Args:
            key: Chave da configuração
            value: Novo valor
        """
        self.data[key] = value
        self.manager.save_guild_settings(self.guild_id, self.data)
    
    def update(self, settings: Dict[str, Any]) -> None:
        """
        Atualiza múltiplas configurações de uma vez
        
        Args:
            settings: Dicionário com as novas configurações
        """
        self.data.update(settings)
        self.manager.save_guild_settings(self.guild_id, self.data)
    
    def delete(self, key: str) -> None:
        """
        Remove uma configuração
        
        Args:
            key: Chave da configuração a remover
        """
        if key in self.data:
            del self.data[key]
            self.manager.save_guild_settings(self.guild_id, self.data)
    
    def __getitem__(self, key: str) -> Any:
        """Permite acessar como dicionário: settings['key']"""
        return self.data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Permite definir como dicionário: settings['key'] = value"""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Permite usar 'in': 'key' in settings"""
        return key in self.data


# Instância global do gerenciador
settings_manager = SettingsManager()
