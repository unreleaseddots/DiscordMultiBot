import discord
from discord.ext import commands

class SlowmodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Você não tem permissões suficientes para ativar o modo lento neste canal.", delete_after=5)
            return False
        return True

    @commands.command(name="slowmode", help="Ativa o modo lento em um canal.")
    async def slowmode(self, ctx, seconds: int):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"O modo lento foi ativado com {seconds} segundos.")

async def setup(bot):
    await bot.add_cog(SlowmodeCog(bot))
