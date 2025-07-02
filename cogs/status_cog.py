import discord
from discord.ext import commands
import requests

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status", help="Mostra informações sobre o bot.")
    async def status(self, ctx):
        # Dados do GitHub
        repo_url = "https://api.github.com/NCKw0lf/nckbot"  # Substitua com seu repositório
        response = requests.get(repo_url)
        if response.status_code == 200:
            data = response.json()
            stars = data.get("stargazers_count", 0)
            forks = data.get("forks_count", 0)
        else:
            stars = "Desconhecido"
            forks = "Desconhecido"

        # Informações do bot
        version = "3.0.0A"  # Altere para a versão atual do seu bot
        team = "Equipe de Desenvolvimento: Nome do Membro 1, Nome do Membro 2"

        await ctx.send(
            f"🤖 **Status do Bot:**\n"
            f"🔧 **Versão:** {version}\n"
            f"👥 **Equipe:** {team}\n"
            f"⭐ **Estrelas no GitHub:** {stars}\n"
            f"🍴 **Forks no GitHub:** {forks}\n"
            f"🌐 **Repositório:** [Link para o repositório](https://github.com/seu_usuario/seu_repositorio)"  # Substitua com o link do seu repositório
        )

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
