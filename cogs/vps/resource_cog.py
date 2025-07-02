import discord
import psutil  # Biblioteca para monitorar recursos do sistema
import socket  # Biblioteca para pegar o IP
from discord.ext import commands
from discord import app_commands

class ResourceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_resource_info(self, channel):
        # Uso de CPU
        cpu_percent = psutil.cpu_percent(interval=1)

        # Uso de memória
        memory_info = psutil.virtual_memory()
        memory_used = memory_info.used / (1024 ** 2)
        memory_total = memory_info.total / (1024 ** 2)

        # Tráfego de rede
        net_info = psutil.net_io_counters()
        bytes_sent = net_info.bytes_sent / (1024 ** 2)
        bytes_recv = net_info.bytes_recv / (1024 ** 2)

        # IP local
        ip_address = socket.gethostbyname(socket.gethostname())

        # Montar a resposta
        response = (
            f"**Uso de Recursos**\n"
            f"CPU: {cpu_percent}%\n"
            f"Memória: {memory_used:.2f} MB / {memory_total:.2f} MB\n"
            f"Tráfego de Rede: \n"
            f" - Enviado: {bytes_sent:.2f} MB\n"
            f" - Recebido: {bytes_recv:.2f} MB\n"
            f"IP Atual: {ip_address}"
        )

        # Verifica se o canal é uma interação ou mensagem normal
        if isinstance(channel, discord.Interaction):
            await channel.response.send_message(response)
        else:
            await channel.send(response)

    # Comando tradicional usando "!"
    @commands.command(name="resource")
    async def resource(self, ctx):
        await self.send_resource_info(ctx)

    # Comando slash "/resource"
    @app_commands.command(name="resource")
    async def resource_slash(self, interaction: discord.Interaction):
        await self.send_resource_info(interaction)

async def setup(bot):
    await bot.add_cog(ResourceCog(bot))
