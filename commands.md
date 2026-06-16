# 📋 Comandos do Bot

## 🚀 Começar aqui

Este arquivo documenta todos os comandos disponíveis do bot Discord.

### Estrutura de Comandos

Para adicionar um novo comando:

1. **Crie um arquivo em `bot/cogs/`** com o nome do comando (ex: `bot/cogs/exemplo.py`)
2. **Defina a classe do Cog** que estende `commands.Cog`
3. **Adicione seus comandos** usando decoradores `@commands.command()` ou `@app_commands.command()`
4. **Registre no `bot/main.py`** (carregamento automático)

### Template de Comando

```python
import discord
from discord.ext import commands

class Exemplo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='exemplo')
    async def exemplo_command(self, ctx):
        \"\"\"Descrição do comando\"\"\"
        await ctx.send("Resposta aqui")

async def setup(bot):
    await bot.add_cog(Exemplo(bot))
```

---

## 📝 Comandos Disponíveis

### 🎲 Sorteio

| Comando | Descrição | Uso |
|---------|-----------|-----|
| `/sorteio` | Sorteia um membro ativo para realizar uma atividade | `/sorteio <atividade> [com_gif]` |

**Parâmetros:**
- `atividade` (obrigatório): A atividade que será realizada
- `com_gif` (opcional): Enviar GIF aleatório? (Padrão: Sim)

**Funcionalidade:**
- Filtra todos os membros online do servidor
- Sorteia um aleatoriamente
- Retorna a mensagem com o membro sorteado
- Se `com_gif` for `Sim`, anexa um GIF de celebração aleatório

**Exemplos:**
```
/sorteio atividade:Fazer um bolo com_gif:Sim
🎲 O usuário @João foi sorteado para Fazer um bolo! [GIF]

/sorteio atividade:Limpar a sala com_gif:Não
🎲 O usuário @Maria foi sorteado para Limpar a sala!
```

---

### ➕ Adicione seus comandos aqui

| Comando | Descrição | Uso |
|---------|-----------|-----|

---

## ⚙️ Configuração

- **Prefixo do bot:** `!`
- **Pasta de comandos:** `bot/cogs/`
- **Arquivo de configuração:** `bot/config.py`
- **Arquivo principal:** `bot/main.py`

---

## 🔧 Desenvolvimento

Para recarregar um comando durante desenvolvimento:
- Edite o arquivo em `bot/cogs/`
- Reinicie o bot
- Os comandos serão sincronizados automaticamente

---

**Última atualização:** 2026-06-15
