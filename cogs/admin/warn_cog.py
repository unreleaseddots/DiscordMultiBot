import discord
from discord.ext import commands

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}  # Dicionário para armazenar os avisos

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Você não tem permissões suficientes para gerenciar avisos.", delete_after=5)
            return False
        return True

    @commands.command(name="warn", help="Avisa um usuário.")
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        if member.id not in self.warns:
            self.warns[member.id] = []
        self.warns[member.id].append(reason or "Nenhuma razão fornecida")
        await ctx.send(f"{member.mention} foi avisado. Motivo: {reason}")

    @commands.command(name="warns", help="Mostra os avisos de um usuário.")
    async def warns(self, ctx, member: discord.Member):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        if member.id in self.warns:
            warn_list = "\n".join(self.warns[member.id])
            await ctx.send(f"{member.mention} tem os seguintes avisos:\n{warn_list}")
        else:
            await ctx.send(f"{member.mention} não tem avisos.")

    @commands.command(name="clearwarns", help="Remove todos os avisos de um usuário.")
    async def clear_warns(self, ctx, member: discord.Member):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        if member.id in self.warns:
            self.warns.pop(member.id)
            await ctx.send(f"Os avisos de {member.mention} foram removidos.")
        else:
            await ctx.send(f"{member.mention} não tem avisos.")

async def setup(bot):
    await bot.add_cog(WarnCog(bot))
