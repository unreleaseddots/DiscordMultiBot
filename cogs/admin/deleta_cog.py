import discord
from discord.ext import commands

class DeletaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deleta", help="Deleta o número especificado de mensagens no canal.")
    async def deleta(self, ctx, quantidade: int):
        # Verificando se o usuário tem permissões necessárias no canal atual
        if not ctx.channel.permissions_for(ctx.author).manage_messages:
            await ctx.send("Você não tem permissão para deletar mensagens.", delete_after=5)
            return

        try:
            deleted = await ctx.channel.purge(limit=quantidade + 1)  # Adiciona 1 para incluir o comando em si
            await ctx.send(f"{len(deleted) - 1} mensagens deletadas.", delete_after=5)
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para deletar mensagens.", delete_after=5)
        except discord.HTTPException:
            await ctx.send("Ocorreu um erro ao tentar deletar as mensagens.", delete_after=5)
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {str(e)}", delete_after=5)

async def setup(bot):
    await bot.add_cog(DeletaCog(bot))
