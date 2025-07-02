import discord
from discord.ext import commands
import yt_dlp
import asyncio
import time


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current_song = None
        self.is_looping = False
        self.volume = 1.0
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.start_time = None  # Guarda o tempo de início da música

    async def ensure_voice(self, ctx):
        """Garante que o bot esteja no canal de voz do usuário."""
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Você precisa estar em um canal de voz para tocar música.")
                return False
        return True

    async def play_next(self, ctx):
        if self.queue:
            self.current_song = self.queue.pop(0)
            url = self.current_song['url']

            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            # Streaming direto do YouTube usando FFmpeg
            voice_client.play(discord.FFmpegOpusAudio(url, **self.ffmpeg_options),
                              after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

            self.start_time = time.time()  # Marca o tempo de início
            await ctx.send(f"Tocando agora: {self.current_song['title']}")
        else:
            self.current_song = None

    async def search_youtube(self, query):
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': 'True',
            'extract_flat': 'True'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return {
                    'title': info['title'],
                    'url': info['url'],
                    'duration': info['duration'],
                    'webpage_url': info['webpage_url']
                }
            except Exception as e:
                print(f"Erro ao buscar no YouTube: {e}")
                return None

    @commands.command(name="play", help="Procura e toca uma música pelo nome.")
    async def play(self, ctx, *, search_query: str = None):
        if search_query is None:
            await ctx.send("Você precisa fornecer o nome da música!")
            return

        # Verifica se o bot está no canal de voz
        if not await self.ensure_voice(ctx):
            return

        search_result = await self.search_youtube(search_query)
        if not search_result:
            await ctx.send("Nenhuma música foi encontrada.")
            return

        song = {'title': search_result['title'], 'url': search_result['url'], 'duration': search_result['duration']}
        self.queue.append(song)

        if not ctx.voice_client.is_playing() and not self.current_song:
            await self.play_next(ctx)
        else:
            await ctx.send(f"Adicionada à fila: {search_result['title']}")

    @commands.command(name="skip", help="Pula para a próxima música.")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.play_next(ctx)

    @commands.command(name="queue", help="Mostra as músicas na fila.")
    async def show_queue(self, ctx):
        if self.queue:
            queue_list = "\n".join([f"{i + 1}. {song['title']}" for i, song in enumerate(self.queue)])
            await ctx.send(f"Fila atual:\n{queue_list}")
        else:
            await ctx.send("A fila está vazia.")

    @commands.command(name="join", help="Entra no canal de voz ou no canal marcado.")
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        if not ctx.voice_client:
            if channel:  # Se um canal for mencionado
                await channel.connect()
                await ctx.send(f"Entrei no canal: {channel.name}")
            elif ctx.author.voice:  # Se o usuário estiver em um canal de voz
                await ctx.author.voice.channel.connect()
                await ctx.send(f"Entrei no canal: {ctx.author.voice.channel.name}")
            else:
                await ctx.send("Você precisa estar em um canal de voz ou marcar um canal para me chamar.")
        else:
            await ctx.send("Já estou conectado a um canal de voz.")

    @commands.command(name="leave", help="Sai do canal de voz.")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Saí do canal de voz.")
        else:
            await ctx.send("Não estou conectado a nenhum canal de voz.")

    @commands.command(name="pause", help="Pausa a música atual.")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada.")

    @commands.command(name="resume", help="Retoma a música pausada.")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música retomada.")

    @commands.command(name="stop", help="Para a música e limpa a fila.")
    async def stop(self, ctx):
        self.queue.clear()
        ctx.voice_client.stop()
        await ctx.send("Música parada e fila limpa.")

    @commands.command(name="remove", help="Remove uma música específica da fila.")
    async def remove(self, ctx, index: int):
        if 0 <= index - 1 < len(self.queue):
            removed = self.queue.pop(index - 1)
            await ctx.send(f"Removida da fila: {removed['title']}")
        else:
            await ctx.send("Índice inválido.")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))