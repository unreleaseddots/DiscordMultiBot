import discord
from discord.ext import commands
import os
import sys

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart", help="Reinicia o bot.")
    async def restart(self, ctx):
        # Verifica se o usuário tem permissões de administrador
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem permissão para reiniciar o bot.")
            return

        await ctx.send("Reiniciando o bot...")
        await self.bot.close()  # Fecha a conexão com o Discord

        # Reinicia o bot
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(RestartCog(bot))
