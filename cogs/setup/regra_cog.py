import discord
from discord.ext import commands
import json
import os


class RegraCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = './message_ids.json'
        self.message_data = {}

        # Carregar os dados do arquivo JSON se existir
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    self.message_data = json.load(file)
                    print(f"Dados carregados: {self.message_data}")
                except json.JSONDecodeError:
                    print("O arquivo JSON está corrompido. Por favor, recrie o arquivo.")

    async def save_message_data(self, guild_id, message_id, channel_id):
        if str(guild_id) not in self.message_data:
            self.message_data[str(guild_id)] = {}

        self.message_data[str(guild_id)]['message_id'] = message_id
        self.message_data[str(guild_id)]['channel_id'] = channel_id

        with open(self.file_path, 'w') as file:
            json.dump(self.message_data, file)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def regras(self, ctx):
        embed = discord.Embed(
            title="Regras da Comunidade",
            description="Por favor, leia as regras abaixo antes de acessar o servidor:",
            color=discord.Color.blue()
        )
        embed.add_field(name="1. Respeito", value="Trate todos com respeito.")
        embed.add_field(name="2. Sem ofensas", value="Ofensas e discriminação não serão toleradas.")
        embed.add_field(name="3. Conteúdo apropriado", value="Não publique conteúdo NSFW.")
        embed.add_field(name="4. Spam", value="Evite spamar mensagens.")
        embed.set_footer(text="Clique no botão abaixo para verificar e ganhar acesso ao servidor.")

        button = discord.ui.Button(label="Verificar", style=discord.ButtonStyle.green, custom_id="verificar")

        async def button_callback(interaction):
            role = discord.utils.get(ctx.guild.roles, name="User's👥")
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("Você agora tem acesso ao servidor!", ephemeral=True)
                print(f"{interaction.user.name} recebeu o cargo '{role.name}'.")
            else:
                await interaction.response.send_message("Cargo não encontrado.", ephemeral=True)

        button.callback = button_callback
        view = discord.ui.View()
        view.add_item(button)

        # Verificar se já existem dados salvos para este servidor
        guild_id = ctx.guild.id
        if str(guild_id) in self.message_data:
            channel_id = self.message_data[str(guild_id)].get('channel_id')
            message_id = self.message_data[str(guild_id)].get('message_id')
            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    # Tentar editar a mensagem existente
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed, view=view)
                    return
                except discord.NotFound:
                    print("Mensagem anterior não encontrada, enviando uma nova.")

        # Se não encontrar, enviar nova mensagem
        message = await ctx.send(embed=embed, view=view)
        await self.save_message_data(guild_id, message.id, ctx.channel.id)

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.data.get('custom_id') == 'verificar':
            role = discord.utils.get(interaction.guild.roles, name="User's👥")
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("Você agora tem acesso ao servidor!", ephemeral=True)
                print(f"{interaction.user.name} recebeu o cargo '{role.name}'.")
            else:
                await interaction.response.send_message("Cargo não encontrado.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(RegraCog(bot))
