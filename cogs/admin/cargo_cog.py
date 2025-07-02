import discord
from discord.ext import commands

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cargo')
    @commands.has_permissions(manage_roles=True)  # Garante que o usuário tenha permissão de gerenciar cargos
    async def add_role(self, ctx, role: discord.Role, member: discord.Member):
        """Adiciona um cargo a um usuário específico."""
        if role in member.roles:
            await ctx.send(f'{member.display_name} já tem o cargo {role.name}.')
        else:
            try:
                await member.add_roles(role)
                await ctx.send(f'{role.name} foi adicionado a {member.display_name}.')
            except discord.Forbidden:
                await ctx.send('Não tenho permissões suficientes para adicionar esse cargo.')
            except discord.HTTPException as e:
                await ctx.send(f'Ocorreu um erro ao adicionar o cargo: {e}')

    @add_role.error
    async def add_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, mencione o cargo e o usuário corretamente. Exemplo: `!cargo @cargo @usuário`')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Cargo ou usuário inválido.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Você não tem permissão para gerenciar cargos.')
        else:
            await ctx.send(f'Ocorreu um erro: {error}')

async def setup(bot):
    await bot.add_cog(RoleManagement(bot))
