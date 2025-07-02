import discord
from discord.ext import commands

class UnmuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("Você não tem permissões suficientes para desmutar este usuário.", delete_after=5)
            return False
        return True

    @commands.command(name="unmute", help="Desmuta um usuário.")
    async def unmute(self, ctx, member: discord.Member):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.mention} foi desmutado(a).")
        else:
            await ctx.send(f"{member.mention} não está mutado(a).")

async def setup(bot):
    await bot.add_cog(UnmuteCog(bot))
