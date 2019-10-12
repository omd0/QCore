from discord import channel
from discord import message

import QCore
from discord.ext import commands
import discord
import youtube_dl

TOKEN = "NDk1MTk0MDgxMDk4NTk2MzYy.XZ3FCQ.VldbvVnzzpTyjSyqDYeo_OmwtPs"

client = commands.Bot(command_prefix= '.')

players = []

@client.event
async def on_ready():
    print('Beep!')

@client.command(pass_context=True)
async def join(ctx):

    await channel.connect()


@client.command(pass_context=True)
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice.clients_in(guild)
    await voice_client.disconnect()

client.run(TOKEN)