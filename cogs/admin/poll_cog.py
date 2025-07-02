import discord
from discord.ext import commands


class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, ctx):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Você não tem permissões suficientes para criar uma enquete.", delete_after=5)
            return False
        return True

    @commands.command(name="poll", help="Cria uma enquete. Use !poll 'Pergunta' 'Opção1' 'Opção2'...")
    async def poll(self, ctx, question: str, *options):
        if not await self.check_permissions(ctx):
            return  # Sai da função se o usuário não tiver permissões

        if len(options) < 2:
            await ctx.send("Você precisa fornecer pelo menos 2 opções.")
            return

        if len(options) > 10:
            await ctx.send("Não pode haver mais que 10 opções.")
            return

        description = []
        for i, option in enumerate(options):
            description.append(f"{i + 1}: {option}")

        embed = discord.Embed(title=question, description="\n".join(description), color=0x00FF00)
        poll_message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(f"{i + 1}\u20E3")  # Adiciona emojis de 1️⃣ a 10️⃣


async def setup(bot):
    await bot.add_cog(PollCog(bot))
