import discord
from discord.ext import commands
import traceback

class Error:
    def __init__(self, bot, reason, description, e=None):
        self.bot = bot
        self.reason = reason
        self.description = description
        self.error = e
        if self.error != None:
            traceback.print_exc(e)

    async def send(self, ctx):
        e = discord.Embed(color=discord.Color.red())
        e.add_field(name=self.reason, value=self.description)
        e.set_footer(text=f"Exception raised by {ctx.author.name}")
        await ctx.send(embed=e)