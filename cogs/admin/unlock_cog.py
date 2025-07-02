import discord
from discord.ext import commands

class UnlockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Você não tem permissões suficientes para desbloquear este canal.", delete_after=5)
            return False
        return True

    @commands.command(name="unlock", help="Desbloqueia um canal.")
    async def unlock(self, ctx):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"{ctx.channel.mention} foi desbloqueado.")

async def setup(bot):
    await bot.add_cog(UnlockCog(bot))
