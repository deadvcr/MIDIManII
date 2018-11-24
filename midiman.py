import discord
from discord.ext import commands
import asyncio
import json
import sys

if not discord.opus.is_loaded():
    discord.opus.load_opus()

with open("config.json") as f:
    config = json.load(f)

cogs = ['cogs.misc', 'cogs.music', 'cogs.info', 'cogs.chan', 'cogs.images']
bot = commands.Bot(command_prefix=config['prefix'], description=config['description'])
#bot.remove_command('help')

if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load {cog}: {e}', file=sys.stderr)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    activity = discord.Game(name=config['activity'])
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run(config['token'], bot=True, reconnect=True)