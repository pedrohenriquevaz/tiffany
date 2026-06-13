# Sunflower Discord Bot

Um bot de Discord desenvolvido em Python com recursos de automatização e jogos.

## Recursos Implementados

### 1. Comando /bump
- Automatização para manter o servidor ativo no Disboard
- Cooldown de 2 horas entre execuções
- Mensagem de feedback ao usuário

### 2. Comando /battle
- Sorteia 2 usuários para um duelo (X1)
- Filtra usuários ativos no dia
- Agrupa usuários por tier (cargo)
- Sistema de reações para confirmação
- Timeout configurável

### 3. Comandos de Configuração
- `/battleChat [canal]` - Define o canal para duelos
- `/prizePool [texto]` - Configura a premiação
- `/setTime [segundos]` - Define tempo limite para resposta
- `/messageRun [mensagem]` - Mensagem de timeout
- `/messageBattle [mensagem]` - Mensagem de início do duelo

## Instalação

1. Clone o repositório
2. Navegue para a pasta `bot/`
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie `.env.example` para `.env` e configure:
   ```
   DISCORD_TOKEN=seu_token_aqui
   GUILD_ID=seu_guild_id_aqui
   ```
5. Execute:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

```
bot/
├── main.py              # Arquivo principal
├── config.py            # Configurações
├── requirements.txt     # Dependências
├── .env.example        # Exemplo de variáveis de ambiente
├── cogs/               # Módulos de funcionalidades
│   ├── bump.py
│   ├── battle.py
│   └── __init__.py
└── utils/              # Utilitários
    ├── database.py     # Gerenciamento de configurações
    └── __init__.py
```

## Próximas Melhorias

- [ ] Banco de dados persistente (SQLite/PostgreSQL)
- [ ] Estatísticas de canais
- [ ] Sistema de XP e ranking
- [ ] Melhor rastreamento de atividade de usuários
- [ ] Comandos de administração avançados

## Requisitos Mínimos

- Python 3.8+
- discord.py 2.0.0+

## Autor

Desenvolvido para o Sunflower Discord Server
