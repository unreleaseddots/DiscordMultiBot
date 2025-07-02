import discord
from discord.ext import commands

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem privilégios suficientes para usar este comando.")
            return False
        return True

    @commands.command(name="ban", help="Banir um usuário.")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not await self.check_admin(ctx):
            return  # Sai da função se o usuário não for administrador

        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} foi banido(a).")

async def setup(bot):
    await bot.add_cog(BanCog(bot))
