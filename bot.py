import discord
import asyncio
import os

#////////debug///////////
#import tracemalloc #debug do codigo
#tracemalloc.start()
#////////debug///////////

from discord.ext import commands
from utils.config import basicconfig

# Definindo as intents, incluindo a intent para o conteúdo das mensagens.
intents = discord.Intents.default()
intents.message_content = True

# Criando a instância do bot com prefixo "!" e as intents necessárias.
bot = commands.Bot(command_prefix=basicconfig.prefix, intents=intents)

# Sincronizando comandos de barra (slash commands)
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sincroniza os comandos de barra com o Discord
    print(f'Bot {bot.user.name} está online! Comandos de barra sincronizados.')

# Função para carregar os cogs, excluindo arquivos __init__.py.
async def loadcogs():
    base_dir = "./cogs"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                cog_path = os.path.join(root, file)[len(base_dir) + 1:-3].replace(os.sep, ".")
                try:
                    await bot.load_extension(f"cogs.{cog_path}")
                    print(f'Cog {cog_path} carregado com sucesso.')
                except Exception as e:
                    print(f'Falha ao carregar {cog_path}: {e}')

# Listener para mensagens que mencionam o bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        command = message.content.replace(f"<@!{bot.user.id}>", "").strip()
        if command.startswith('!'):
            command = command[1:]
            ctx = await bot.get_context(message)
            await bot.invoke(ctx)
    await bot.process_commands(message)

# Executando o bot e carregando os cogs
asyncio.run(loadcogs())
bot.run(basicconfig.token)