import discord
from discord.ext import commands

class RemoveRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("Você não tem permissões suficientes para remover cargos.", delete_after=5)
            return False
        return True

    @commands.command(name="removecargo", help="Remove um cargo de um usuário.")
    async def remove_cargo(self, ctx, member: discord.Member, role: discord.Role):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"O cargo {role.name} foi removido de {member.mention}.")
        else:
            await ctx.send(f"O usuário {member.mention} não possui o cargo {role.name}.")

async def setup(bot):
    await bot.add_cog(RemoveRoleCog(bot))
