import discord
from discord.ext import commands

class LockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem privilégios suficientes para usar este comando.")
            return False
        return True

    @commands.command(name="lock", help="Bloqueia um canal.")
    async def lock(self, ctx):
        if not await self.check_admin(ctx):
            return  # Sai da função se o usuário não for administrador

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"{ctx.channel.mention} foi bloqueado.")

async def setup(bot):
    await bot.add_cog(LockCog(bot))
