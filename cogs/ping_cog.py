import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

# Adicionar o cog ao bot
async def setup(bot):
    await bot.add_cog(Ping(bot))
