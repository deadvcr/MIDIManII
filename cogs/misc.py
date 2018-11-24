import discord
from discord.ext import commands
from .utils import error
import aiohttp
import random
import requests
import json

async def webrequest(self, ctx, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                rbody = await r.text()
                return rbody
            else:
                await error.Error(self.bot, "Something went wrong.", "The web request could not be completed. Please try again.").send(ctx)
        


class Misc:
    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.command()
    async def help(self, ctx):
        msg = discord.Embed(title="Help List",
                            description="See the full command list at http://deadvcr.com/midiman",
                            color=discord.Color.gold())
        await ctx.send(embed=msg)
    '''



    @commands.command()
    async def god(self, ctx):
        '''
        Speak with God himself.
        ''' 
        resp = await webrequest(self.bot, ctx, "http://templeos.net/")    
        msg = discord.Embed(
            title="Talk to God!",
            description=f"{resp}",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=msg)

    @commands.command()
    async def invite(self, ctx):
        '''
        Invite to your server
        '''
        msg = discord.Embed(
            title="Invite MIDI Man",
            description="Invite him to the server using the following link:\nhttps://discordapp.com/oauth2/authorize?client_id=514910351683223563&scope=bot&permissions=0",
            color=discord.Color.purple()
        )
        msg.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=msg)

    @commands.command()
    async def jeffbin(self, ctx):
        data = await webrequest(self.bot, ctx, "http://infowars.info/random.php")
        info = (data[:1000] + '[...]\n[too long for Discord]') if len(data) > 1000 else data

        msg = discord.Embed(color=discord.Color.dark_green())
        msg.add_field(
            name="Random JeffBin Post",
            value=f"{info}",
        )
        msg.set_footer(text="Submit your own at https://infowars.info/")

        await ctx.send(embed=msg)


    @commands.command()
    async def magic8(self, ctx):
        '''
        Roll the magic 8 ball
        '''
        replies = [
            "It is certain",
            "It is decidedly so",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Without a doubt",
            "Reply hazy, try again.",
            "Don't count on it",
            "No.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        choice = random.choice(replies)
        msg = discord.Embed(
            title="Magic 8 Ball",
            description=choice,
            color = discord.Color.green()
        )
        await ctx.send(embed=msg)  

    @commands.command()
    async def ud(self, ctx, *, query):
        word = query.strip()
        url = "http://api.urbandictionary.com/v0/define?term={"+word+"}"
        try:
            resp = requests.get(url=url)
            data = resp.json()
        except Exception as e:
            await error.Error(self.bot, "There was an error during the request", e).send(ctx)
            return None
        if len(data['list']) == 0:
            await ctx.send(embed=discord.Embed(title="No definition available",description="Please try another search term."))
            return None
        definition = data['list'][0]['definition']
        info = (definition[:900] + '[...]\n[too long for Discord]') if len(definition) > 900 else definition
        permalink = data['list'][0]['permalink']
        votes = data['list'][0]['thumbs_up']

        msg = discord.Embed(color=discord.Color.orange())
        msg.set_author(name=word, url=permalink)
        msg.add_field(name='Definition', value=info, inline=False)
        msg.add_field(name='Upvotes', value=votes, inline=False)

        await ctx.send(embed=msg)




def setup(bot):
    bot.add_cog(Misc(bot))