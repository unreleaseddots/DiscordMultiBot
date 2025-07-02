import discord
from discord.ext import commands

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem privilégios suficientes para usar este comando.")
            return False
        return True

    @commands.command(name="mute", help="Mute um usuário.")
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if not await self.check_admin(ctx):
            return  # Sai da função se o usuário não for administrador

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"{member.mention} foi mutado(a).")

async def setup(bot):
    await bot.add_cog(MuteCog(bot))
