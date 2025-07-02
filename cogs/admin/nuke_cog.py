import discord
from discord.ext import commands

class NukeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Você não tem privilégios suficientes para usar este comando.", delete_after=5)
            return False
        return True

    @commands.command(name="nuke", help="Nuke o canal atual.")
    async def nuke(self, ctx):
        # Verificando se o usuário tem permissões necessárias no canal atual
        if not await self.check_admin(ctx):
            return  # Sai da função se o usuário não for administrador

        channel = ctx.channel
        await ctx.send("Iniciando o processo de nuke...")

        # Criar um novo canal com as mesmas configurações
        new_channel = await channel.category.create_text_channel(
            name=channel.name,
            overwrites=channel.overwrites
        )

        # Mover o novo canal para a mesma posição que o antigo
        await new_channel.edit(position=channel.position)

        # Deletar o canal antigo
        await channel.delete()

        await new_channel.send("Canal nukeado com sucesso!")

async def setup(bot):
    await bot.add_cog(NukeCog(bot))
