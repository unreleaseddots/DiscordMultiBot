import discord
from discord.ext import commands

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1289236895741644830  # ID do canal de logs
        self.logging_enabled = True  # Variável para lembrar o estado dos logs

    async def get_log_channel(self, guild):
        return guild.get_channel(self.log_channel_id)  # Obtém o canal pelo ID

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.logging_enabled:
            channel = await self.get_log_channel(member.guild)
            if channel:
                await channel.send(f"{member.name} entrou no servidor.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.logging_enabled:
            channel = await self.get_log_channel(member.guild)
            if channel:
                await channel.send(f"{member.name} saiu do servidor.")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if self.logging_enabled:
            channel = await self.get_log_channel(guild)
            if channel:
                await channel.send(f"{user.name} foi banido.")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if self.logging_enabled:
            channel = await self.get_log_channel(guild)
            if channel:
                await channel.send(f"{user.name} foi desbanido.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.logging_enabled:
            channel = await self.get_log_channel(after.guild)
            if channel:
                if before.display_name != after.display_name:
                    await channel.send(f"{before.name} mudou o nome para {after.display_name}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.logging_enabled:
            if message.author == self.bot.user:  # Ignora mensagens do bot
                return
            channel = await self.get_log_channel(message.guild)
            if channel:
                await channel.send(f"{message.author.name} enviou uma mensagem: {message.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.logging_enabled:
            if message.author == self.bot.user:  # Ignora mensagens do bot
                return
            channel = await self.get_log_channel(message.guild)
            if channel:
                await channel.send(f"{message.author.name} deletou uma mensagem: {message.content}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.logging_enabled:
            if user == self.bot.user:  # Ignora reações do bot
                return
            channel = await self.get_log_channel(reaction.message.guild)
            if channel:
                await channel.send(f"{user.name} reagiu com {reaction.emoji} em uma mensagem.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.logging_enabled:
            channel = await self.get_log_channel(member.guild)
            if channel:
                if before.channel is None and after.channel is not None:
                    await channel.send(f"{member.name} entrou no canal de voz {after.channel.name}.")
                elif before.channel is not None and after.channel is None:
                    await channel.send(f"{member.name} saiu do canal de voz {before.channel.name}.")
                elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                    await channel.send(f"{member.name} mudou do canal de voz {before.channel.name} para {after.channel.name}.")

class DisableLoggingCog(commands.Cog):
    def __init__(self, bot, logging_cog: LoggingCog):
        self.bot = bot
        self.logging_cog = logging_cog

    @commands.command(name='disable_logs', help='Desabilita os logs.')
    async def disable_logs(self, ctx):
        self.logging_cog.logging_enabled = False
        await ctx.send("Logs desabilitados.")

    @commands.command(name='enable_logs', help='Habilita os logs.')
    async def enable_logs(self, ctx):
        self.logging_cog.logging_enabled = True
        await ctx.send("Logs habilitados.")

async def setup(bot):
    logging_cog = LoggingCog(bot)
    await bot.add_cog(logging_cog)
    await bot.add_cog(DisableLoggingCog(bot, logging_cog))
