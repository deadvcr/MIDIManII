import discord
from discord.ext import commands
from discord.utils import get
import traceback

class Loading:
    def __init__(self, bot, reason):
        self.bot = bot
        self.reason = reason
        self.msg = None

    async def send(self, ctx):
        emoji = get(self.bot.emojis, id=514288515215917057)
        e = discord.Embed(title=f"{emoji}{self.reason}", color=discord.Color.blurple())
        self.msg = await ctx.send(embed=e)
    
    async def delete(self):
        await self.msg.delete()