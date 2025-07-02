import discord
from discord.ext import commands

class AutoRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="User's👥")  # Substitua por um nome de cargo existente
        if role:
            await member.add_roles(role)
            try:
                await member.send(f"Bem-vindo ao servidor {member.guild.name}! Você recebeu o cargo {role.name}.")
            except discord.Forbidden:
                print(f"Não consegui enviar uma mensagem para {member.name}. Ele pode ter as mensagens diretas desativadas.")

async def setup(bot):
    await bot.add_cog(AutoRoleCog(bot))
