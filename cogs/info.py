import asyncio
import discord
from discord.ext import commands
from PIL import Image


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Find information of anyone in the server")
    async def whois(self, ctx, *, user:discord.Member=None):
        if user is None:
            user = ctx.author
        msg = discord.Embed(title = "Whois",
                            description="Name: " + str(user.name) +'\n' + "ID: " + str(user.id) + "\nDiscriminator: " + str(user.discriminator) + "\nCreated on: " + str(user.created_at) + "\nStatus: " + str(user.status) + "\nJoined: " + str(user.joined_at) + "\nBot: " + str(user.bot),
                            color = discord.Color.blue())
        msg.set_thumbnail(url=user.avatar_url)                    
        await ctx.send(embed=msg)

    @commands.command(description="Post the avatar of a specified person")
    async def avatar(self, ctx, *, user:discord.User=None):
        if user is None:
            user = ctx.author
        msg = discord.Embed(title="Avatar",
                            color = discord.Color.blue())
        msg.set_image(url=user.avatar_url)
        await ctx.send(embed=msg)

    @commands.command(description="Get the current song that you or another user is playing")
    async def spotify(self, ctx, user:discord.Member=None):
        """Get the current song that you or another user is playing"""
        if user is None:
            user = ctx.author
        activity = ctx.author.activity
        if activity is None:
            await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
            return
        if activity.type == discord.ActivityType.listening and activity.name == "Spotify":
            embed = discord.Embed(description="\u200b")
            embed.add_field(name="Artists", value=", ".join(activity.artists))
            embed.add_field(name="Album", value=activity.album)
            embed.add_field(name="Duration", value=str(activity.duration)[3:].split(".", 1)[0])
            embed.title = "**{}**".format(activity.title)
            embed.set_thumbnail(url=activity.album_cover_url)
            embed.url = "https://open.spotify.com/track/{}".format(activity.track_id)
            embed.color = activity.color
            embed.set_footer(text="{} - is currently playing this song".format(ctx.author.display_name))
            await ctx.send(embed=embed)
        else:
            await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
            return

    @commands.command()
    async def color(self, ctx, *, hexcode:str):
        """Displays the given hex color"""
        await ctx.channel.trigger_typing()
        if not hexcode.startswith("#"):
            hexcode = "#{}".format(hexcode)
        try:
            Image.new("RGBA", (50, 50), hexcode).save("data/color.png")
        except ValueError:
            await ctx.send("Invalid color.")
            return
        await ctx.send(file=discord.File("data/color.png", "{}.png".format(hexcode.strip("#"))))

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        person_count = len([member for member in guild.members if not member.bot])
        bot_count = len([member for member in guild.members if member.bot])
        msg = "ID: " + str(guild.id) + "\nCreated on: " + str(guild.created_at) + "\nRegion: " + str(guild.region) + "\nMember count: " + str(len(guild.members)) + ". " + str(person_count) + " are humans and " + str(bot_count) + " are bots." + "\nOwner: " + str(guild.owner) + "\n"
        embed = discord.Embed(description=msg,
                            color=discord.Color.green())
        embed.title = guild.name
        if guild.icon_url:
            embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)
            

        
def setup(bot):
    bot.add_cog(Info(bot))
    print('Info module is loaded')
