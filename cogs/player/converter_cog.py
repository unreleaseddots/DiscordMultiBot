import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import asyncio

class ConverterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mp3", help="Converte um vídeo do YouTube para MP3")
    async def convert(self, ctx, url: str):
        output_path = 'downloads'
        # Verificando se a pasta de downloads existe
        os.makedirs(output_path, exist_ok=True)

        await ctx.send("Iniciando o download e a conversão para MP3...")

        # Definindo opções do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,  # Não baixar playlists
        }

        # Função para baixar e converter (não assíncrona)
        def download_and_convert():
            try:
                # Baixando e convertendo o áudio
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    title = info_dict.get('title', None)
                    file_name = f"{output_path}/{title}.mp3"

                return file_name

            except youtube_dl.DownloadError as e:
                raise Exception(f"Ocorreu um erro durante o download: {str(e)}")
            except Exception as e:
                raise Exception(f"Ocorreu um erro inesperado: {str(e)}")

        # Executando a função de download em um executor
        loop = asyncio.get_running_loop()
        try:
            file_name = await loop.run_in_executor(None, download_and_convert)
            await ctx.send("Conversão concluída! O arquivo MP3 está sendo enviado...")
            await ctx.send(file=discord.File(file_name))

            # Removendo o arquivo após o envio
            os.remove(file_name)

        except Exception as e:
            await ctx.send(str(e))

# Configurando o Cog no bot
async def setup(bot):
    await bot.add_cog(ConverterCog(bot))
