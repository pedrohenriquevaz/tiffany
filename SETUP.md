## 🚀 Guia de Setup - Sunflower Discord Bot

### Pré-requisitos
- Python 3.8 ou superior instalado
- Uma aplicação Discord criada em https://discord.com/developers/applications
- Permissão de administrador no servidor Discord onde será testado

---

## 📋 Passo a Passo

### 1. Obter o Token do Bot
1. Acesse https://discord.com/developers/applications
2. Clique em "New Application" e dê um nome (ex: Sunflower)
3. Vá para a aba "Bot" → "Add Bot"
4. Em "TOKEN", clique "Copy" (este é seu `DISCORD_TOKEN`)
5. Certifique-se que as seguintes intents estão ativadas:
   - Message Content Intent
   - Server Members Intent
   - Guild Members Intent

### 2. Obter o Guild ID
1. Abra seu servidor Discord
2. Ative o "Modo de Desenvolvedor" (User Settings → Advanced → Developer Mode)
3. Clique com botão direito no nome do servidor → "Copy Server ID" (este é seu `GUILD_ID`)

### 3. Adicionar o Bot ao Servidor
1. Ainda em https://discord.com/developers/applications
2. Vá para "OAuth2" → "URL Generator"
3. Selecione os escopos: `bot`
4. Selecione as permissões:
   - Send Messages
   - Embed Links
   - Add Reactions
   - Read Message History
   - Manage Messages
5. Copie a URL gerada e abra no navegador
6. Selecione o servidor e autorize

### 4. Configurar o Arquivo .env
Na pasta `bot/`, crie um arquivo `.env` com:
```
DISCORD_TOKEN=seu_token_aqui
GUILD_ID=seu_guild_id_aqui
```

**⚠️ IMPORTANTE**: Nunca compartilhe seu token publicamente!

### 5. Instalar Dependências
```bash
cd bot
pip install -r requirements.txt
```

### 6. Executar o Bot
```bash
python main.py
```

Você verá algo como:
```
✅ Cog bump carregado com sucesso!
✅ Cog battle carregado com sucesso!
Bot Sunflower#1234 está online!
Sincronizados 7 slash commands
```

---

## 🎮 Usando os Comandos

### Configuração Inicial (Admin Only)

1. **Definir Canal de Duelos**
   ```
   /battleChat [canal]
   ```

2. **Configurar Premiação**
   ```
   /prizePool Descrição da premiação aqui
   ```

3. **Definir Tempo Limite**
   ```
   /setTime 60
   ```

4. **Mensagens Customizadas**
   ```
   /messageRun Mensagem de timeout
   /messageBattle Mensagem de início do duelo
   ```

### Comandos de Uso Geral

1. **Executar Bump**
   ```
   /bump
   ```

2. **Iniciar Duelo**
   ```
   /battle
   ```

---

## 📝 Notas Importantes

- Os usuários precisam ter um dos seguintes cargos para participar de duelos:
  - 🎴ㅤÉpico
  - 🀄ㅤLenda
  - 🌗ㅤMítico
  - 🌗ㅤHonra
  - 🌓ㅤGlória
  - 🌒ㅤImortal

- O sistema de atividade (duelos) está simplificado nesta versão. Em produção, será necessário rastrear:
  - Mensagens enviadas
  - Atividades em chamadas de voz

- As configurações são armazenadas em memória. Para persistência, implemente um banco de dados (SQLite, PostgreSQL, etc.)

---

## 🐛 Troubleshooting

### Slash commands não aparecem
- Aguarde alguns minutos
- Recarregue o Discord (Ctrl+R)
- Verifique se o bot está online

### Bot não responde
- Verifique se o token está correto em `.env`
- Certifique-se de que o bot tem permissões necessárias

### Erro "Token is invalid"
- Verifique se copiou o token corretamente
- Regenere um novo token se necessário

---

## 📚 Próximos Passos

1. Implementar banco de dados para persistência
2. Adicionar sistema de estatísticas de canais
3. Implementar rastreamento de atividade real
4. Adicionar sistema de ranking/XP
5. Criar painel de administração

---

Boa sorte com seu bot! 🎉
