import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ajuda", help="Mostra este menu de ajuda")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Menu de Ajuda",
            description="Lista de comandos disponíveis:",
            color=discord.Color.blue()
        )

        for command in self.bot.commands:
            embed.add_field(
                name=f"!{command.name}",
                value=command.help,
                inline=False
            )

        await ctx.send(embed=embed)

# Configurando o Cog no bot
async def setup(bot):
    await bot.add_cog(HelpCog(bot))