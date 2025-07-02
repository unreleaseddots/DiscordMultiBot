import discord
from discord.ext import commands
import random

class Player:
    def __init__(self, user):
        self.user = user
        self.cards = []
        self.standing = False  # Indica se o jogador decidiu parar

    def hand_value(self):
        total = 0
        aces = 0
        for card in self.cards:
            if card == 11:  # Ás
                aces += 1
            elif card > 10:  # J, Q, K
                total += 10
            else:
                total += card

        # Adiciona o valor do Ás, podendo ser 1 ou 11
        for _ in range(aces):
            if total + 11 > 21:
                total += 1
            else:
                total += 11
        return total

class BlackjackGame:
    def __init__(self, player1, player2, channel):
        self.player1 = player1
        self.player2 = player2
        self.channel = channel
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # Baralho de 52 cartas
        random.shuffle(self.deck)
        self.started = False

    def deal_card(self, player):
        card = self.deck.pop(0)
        player.cards.append(card)

    def is_game_over(self):
        return self.player1.standing and self.player2.standing or self.player1.hand_value() > 21 or self.player2.hand_value() > 21

    def determine_winner(self):
        if self.player1.hand_value() > 21:
            return f"{self.player1.user.display_name} estourou com {self.player1.hand_value()}! {self.player2.user.display_name} venceu!"
        elif self.player2.hand_value() > 21:
            return f"{self.player2.user.display_name} estourou com {self.player2.hand_value()}! {self.player1.user.display_name} venceu!"
        elif self.player1.hand_value() == self.player2.hand_value():
            return f"Empate! Ambos têm {self.player1.hand_value()}."
        elif self.player1.hand_value() > self.player2.hand_value():
            return f"{self.player1.user.display_name} venceu com {self.player1.hand_value()} contra {self.player2.user.display_name} que tem {self.player2.hand_value()}."
        else:
            return f"{self.player2.user.display_name} venceu com {self.player2.hand_value()} contra {self.player1.user.display_name} que tem {self.player1.hand_value()}."

games = {}

class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="21", help="Inicia um jogo de 21")
    async def start_game(self, ctx):
        if ctx.author.id in games:
            await ctx.send("Você já está em um jogo!", ephemeral=True)
            return

        # Cria um botão para outro jogador se juntar
        view = discord.ui.View(timeout=None)
        button = discord.ui.Button(label="Entrar no jogo", style=discord.ButtonStyle.green)
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.send_message("Você não pode se juntar ao seu próprio jogo!", ephemeral=True)
                return

            if interaction.user.id in games:
                await interaction.response.send_message("Você já está em um jogo!", ephemeral=True)
                return

            # Cria um canal temporário onde só os dois jogadores têm acesso
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ctx.author: discord.PermissionOverwrite(view_channel=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True),
                ctx.guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            channel = await ctx.guild.create_text_channel(f"21-{ctx.author.name}-vs-{interaction.user.name}", overwrites=overwrites)

            player1 = Player(ctx.author)
            player2 = Player(interaction.user)

            # Registra o jogo
            game = BlackjackGame(player1, player2, channel)
            games[ctx.author.id] = game
            games[interaction.user.id] = game

            await interaction.response.send_message(f"Você entrou no jogo com {ctx.author.display_name}!", ephemeral=True)
            await channel.send(f"{ctx.author.mention} e {interaction.user.mention}, o jogo de 21 começou!")

            # Exibe as regras e os comandos
            rules_message = (
                "**Bem-vindos ao jogo de 21 (Blackjack)!**\n\n"
                "**Regras básicas:**\n"
                "1. O objetivo é somar as cartas e ficar o mais próximo possível de 21, sem ultrapassar.\n"
                "2. Cartas de 2 a 10 têm valor nominal, J, Q, K valem 10, e o Ás (A) vale 1 ou 11.\n"
                "3. Se o valor total das suas cartas ultrapassar 21, você perde automaticamente (estoura).\n"
                "4. Cada jogador pode `!hit` para pedir mais cartas ou `!stand` para parar.\n"
                "5. O vencedor será o jogador que tiver a mão mais próxima de 21 sem estourar.\n\n"
                "**Comandos do jogo:**\n"
                "`!hit` - Pede mais uma carta.\n"
                "`!stand` - Para de pedir cartas e espera o resultado.\n"
                "`!cartas` - Ver as suas cartas atuais.\n\n"
                "Boa sorte!"
            )
            await channel.send(rules_message)

            # Distribui as cartas iniciais
            game.deal_card(player1)
            game.deal_card(player1)
            game.deal_card(player2)
            game.deal_card(player2)

            await channel.send(f"Cartas foram distribuídas! Use `!hit` para pedir mais cartas ou `!stand` para parar.")
            await ctx.send(f"O jogo começou! Vá para {channel.mention} para continuar.", ephemeral=True)

        button.callback = button_callback
        await ctx.send("Clique para entrar no jogo de 21!", view=view, ephemeral=True)

    @commands.command(name="hit", help="Pedir mais uma carta.")
    async def hit(self, ctx):
        if ctx.author.id not in games:
            await ctx.send("Você não está em um jogo!", ephemeral=True)
            return

        game = games[ctx.author.id]
        player = game.player1 if game.player1.user == ctx.author else game.player2

        if player.standing:
            await ctx.send("Você já decidiu parar!", ephemeral=True)
            return

        game.deal_card(player)
        value = player.hand_value()

        if value > 21:
            await ctx.send(f"Você tirou {player.cards[-1]} e agora tem {value}. Você estourou!", ephemeral=True)
        else:
            await ctx.send(f"Você tirou {player.cards[-1]} e agora tem {value}.", ephemeral=True)

        if game.is_game_over():
            winner_message = game.determine_winner()
            await game.channel.send(winner_message)
            await game.channel.delete()
            del games[game.player1.user.id]
            del games[game.player2.user.id]

    @commands.command(name="stand", help="Parar de pedir cartas.")
    async def stand(self, ctx):
        if ctx.author.id not in games:
            await ctx.send("Você não está em um jogo!", ephemeral=True)
            return

        game = games[ctx.author.id]
        player = game.player1 if game.player1.user == ctx.author else game.player2

        player.standing = True
        await ctx.send("Você decidiu parar.", ephemeral=True)

        if game.is_game_over():
            winner_message = game.determine_winner()
            await game.channel.send(winner_message)
            await game.channel.delete()
            del games[game.player1.user.id]
            del games[game.player2.user.id]

    @commands.command(name="cartas", help="Ver suas cartas no jogo.")
    async def show_cards(self, ctx):
        if ctx.author.id not in games:
            await ctx.send("Você não está em um jogo!", ephemeral=True)
            return

        game = games[ctx.author.id]
        player = game.player1 if game.player1.user == ctx.author else game.player2

        cards = ', '.join(map(str, player.cards))
        await ctx.send(f"Suas cartas: {cards} (Total: {player.hand_value()})", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BlackjackCog(bot))
