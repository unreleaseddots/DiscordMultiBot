import discord
from discord.ext import commands
from discord import ButtonStyle
from discord.ui import Button, View
import datetime  # Para registrar a data e hora no log
from discord.ext.commands import cooldown, BucketType

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_cooldowns = {}  # Dicionário para armazenar cooldowns de criação de tickets
        self.notify_cooldowns = {}  # Dicionário para cooldowns de chamar suporte

    # Comando para criar o embed de suporte com o botão
    @commands.command()
    async def ticket(self, ctx):
        embed = discord.Embed(
            title="Sistema de Tickets de Suporte",
            description="Clique no botão abaixo para abrir um ticket e falar com a equipe de suporte!",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url="https://i.imgur.com/8eJpfNA.png")  # URL de uma imagem ou logo
        embed.set_footer(text="Obrigado por usar nosso sistema de suporte!")

        button = Button(label="Abrir Ticket", style=ButtonStyle.green, custom_id="open_ticket")

        view = View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    # Função para capturar a interação quando o botão for clicado
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        user = interaction.user

        if interaction.data['custom_id'] == "open_ticket":
            # Verificar cooldown de abertura de ticket
            if user.id in self.ticket_cooldowns:
                cooldown_end = self.ticket_cooldowns[user.id]
                if datetime.datetime.now() < cooldown_end:
                    time_remaining = (cooldown_end - datetime.datetime.now()).seconds // 60
                    await interaction.response.send_message(
                        f"Você precisa esperar {time_remaining} minutos antes de abrir outro ticket.",
                        ephemeral=True)
                    return
            # Definir cooldown de 30 minutos
            self.ticket_cooldowns[user.id] = datetime.datetime.now() + datetime.timedelta(minutes=30)

            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="Tickets")
            if category is None:
                category = await guild.create_category("Tickets")

            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{user.name}",
                category=category,
                topic=f"Ticket de {user.name}"
            )

            await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
            await ticket_channel.set_permissions(guild.default_role, read_messages=False)

            await ticket_channel.send(
                content=f"{user.mention}, seu ticket foi criado! Um membro da equipe de suporte irá atendê-lo em breve.",
                embed=discord.Embed(
                    title="Ticket de Suporte",
                    description="Explique seu problema ou dúvida. A equipe de suporte estará com você em breve!",
                    color=discord.Color.green()
                )
            )

            # Criando botões para fechar o ticket e chamar suporte
            close_button = Button(label="Fechar Ticket", style=ButtonStyle.red, custom_id="close_ticket")
            notify_button = Button(label="Chamar Suporte", style=ButtonStyle.secondary, custom_id="notify_support")

            # Criando a view para os botões
            view = View()
            view.add_item(close_button)
            view.add_item(notify_button)

            # Adicionando os botões ao canal do ticket
            await ticket_channel.send(view=view)

            await interaction.response.send_message(
                f"Seu ticket foi criado: {ticket_channel.mention}",
                ephemeral=True
            )

        elif interaction.data['custom_id'] == "close_ticket":
            ticket_channel = interaction.channel
            # Verificar se o usuário tem permissão de administrador ou é o criador do ticket
            if user.guild_permissions.administrator or ticket_channel.topic.startswith(f"Ticket de {user.name}"):
                # Logando o fechamento do ticket
                with open("ticket_logs.txt", "a") as log_file:
                    log_file.write(
                        f"{datetime.datetime.now()}: Ticket {ticket_channel.name} fechado por {user.name}.\n")

                await ticket_channel.send("Este ticket foi fechado.")
                await ticket_channel.delete()
            else:
                await interaction.response.send_message("Você não tem permissão para fechar este ticket.",
                                                        ephemeral=True)

        elif interaction.data['custom_id'] == "notify_support":
            # Verificar cooldown de chamar suporte
            if user.id in self.notify_cooldowns:
                cooldown_end = self.notify_cooldowns[user.id]
                if datetime.datetime.now() < cooldown_end:
                    time_remaining = (cooldown_end - datetime.datetime.now()).seconds // 60
                    await interaction.response.send_message(
                        f"Você precisa esperar {time_remaining} minutos antes de chamar o suporte novamente.",
                        ephemeral=True)
                    return
            # Definir cooldown de 30 minutos
            self.notify_cooldowns[user.id] = datetime.datetime.now() + datetime.timedelta(minutes=30)

            support_role = discord.utils.get(interaction.guild.roles,
                                             name="Suporte")  # Substitua pelo nome do seu cargo de suporte
            if support_role:
                await interaction.channel.send(
                    f"{support_role.mention}, um novo ticket foi aberto por {interaction.user.mention}!")

            await interaction.response.send_message("O suporte foi notificado.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
