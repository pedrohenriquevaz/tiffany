# Discord Bot - Versão Renovada

Um bot de Discord desenvolvido em Python pronto para desenvolvimento de novas funcionalidades.

## ℹ️ Sobre

Este é o núcleo base do bot com todos os sistemas legados removidos. Está pronto para que você adicione novos comandos e funcionalidades conforme necessário.

## 📖 Documentação

Para ver a lista de comandos e como criar novos, consulte [../commands.md](../commands.md)

## 🚀 Instalação

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
