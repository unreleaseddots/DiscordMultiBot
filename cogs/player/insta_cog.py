import discord
from discord.ext import commands
import yt_dlp
import os
import shutil
import asyncio


class InstaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download_video(self, url: str, ydl_opts: dict):
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
        return info

    @commands.command(name='insta', help='Baixa um Reel do Instagram e envia no chat.')
    async def insta(self, ctx, url: str):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(id)s/%(id)s.%(ext)s',  # Salva na pasta com o ID do vídeo
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Formato do vídeo
            }]
        }

        video_id = None  # Definindo video_id como None inicialmente

        try:
            # Baixar o vídeo de forma assíncrona
            info = await self.download_video(url, ydl_opts)
            video_id = info.get('id')  # Verifica se o 'id' está presente
            if not video_id:
                raise ValueError("ID do vídeo não encontrado.")

            video_path = f"{video_id}/{video_id}.mp4"

            # Verifica se o vídeo foi baixado com sucesso
            if os.path.exists(video_path):
                await ctx.send(file=discord.File(video_path))  # Envia o vídeo
            else:
                raise FileNotFoundError(f"Vídeo não encontrado no caminho {video_path}")

        except yt_dlp.utils.DownloadError as e:
            await ctx.send(f"Erro ao baixar o vídeo: {str(e)}")
        except FileNotFoundError as e:
            await ctx.send(f"Erro: {str(e)}")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {str(e)}")
        finally:
            # Garante que a pasta seja removida, mesmo em caso de erro, apenas se o video_id foi definido
            if video_id and os.path.exists(video_id):
                shutil.rmtree(video_id)


async def setup(bot):
    await bot.add_cog(InstaCog(bot))
