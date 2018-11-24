import discord
from discord.ext import commands
import os, random
from PIL import Image, ImageDraw, ImageFont
import time
import textwrap
import json
from .utils import error, loading
class Images:
    def __init__(self, bot):
        self.bot = bot
        self.sep = "|"
        # load images
        images_file = open("static/images/meme_tpl/images.json")
        images_str = images_file.read()
        self.images = json.loads(images_str)

    @commands.command(name="gen")
    async def _meme_gen(self, ctx, meme, *, text=None):
        """Generate images with input text.
        Parameters
        ------------
        meme: str [Required]
            Name of the image you want to generate. (Can also be 'list' to get a list of generatable images.)
        text: str [Required]
            Image's arguments separated by '|'.
        """
        images = self.images["images"]

        if meme == None:
            await error.Error(self.bot, "You did not supply an image", f"Please follow the syntax: `!gen <image> <...args>`. You can get a list of images with `!genlist`.").send(ctx)
            return
        elif meme == "list":
            e = discord.Embed(title="Image Generation List", color=discord.Color.blurple())
            for imageDict in images:
                name = imageDict["name"]
                desc = imageDict["desc"]
                flen = len(imageDict["subImages"])
                e.add_field(name=name, value=f"{desc} ({flen})")
            await ctx.send(content=None, embed=e)
            return
        for imageDict in images:
            if imageDict["name"] == meme:
                loadingMessage = loading.Loading(self.bot, "Generating your image...")
                await loadingMessage.send(ctx)
                if text.lower() == "example":
                    if len(imageDict["exampleValues"]) == 1:
                        text = "".join(imageDict["exampleValues"])
                    else:
                        text = "|".join(imageDict["exampleValues"])
                try:
                    im = Image.open(f"static/images/meme_tpl/{imageDict['folder']}/{imageDict['fileName']}")
                    sub_images = []
                    for sub_image in imageDict["subImages"]:
                        sub_images.append(sub_image)
                except Exception as e:
                    await error.Error(self.bot, "Could not load image", "The requested image could not be loaded. Please try again later.", e).send(ctx)
                    return
                draw_main = ImageDraw.Draw(im)
                text_args = text.split(self.sep)
                if len(text_args) != len(imageDict["subImages"]):
                    await error.Error(self.bot, "Invalid arguments supplied", f"`{imageDict['name']}` expects {len(imageDict['subImages'])}, not {len(text_args)}.").send(ctx)
                for k, v in enumerate(sub_images):
                    text = textwrap.wrap(text_args[k], width=v["font"]["fontWidth"])
                    text = '\n'.join(text)
                    font = ImageFont.truetype(f"static/fonts/{v['font']['name']}.ttf", v['font']['size'])
                    if 'outlineThickness' in v['font']:
                        outlineAmount = v['font']['outlineThickness']
                        for adj in range(outlineAmount):
                            draw_main.text((v['pos'][0]-adj, v['pos'][1]), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0]+adj, v['pos'][1]), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0], v['pos'][1]+adj), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0], v['pos'][1]-adj), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0]-adj, v['pos'][1]+adj), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0]+adj, v['pos'][1]+adj), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0]-adj, v['pos'][1]-adj), text, font=font, fill=v['font']['outlineColour'])
                            draw_main.text((v['pos'][0]+adj, v['pos'][1]-adj), text, font=font, fill=v['font']['outlineColour'])
                    draw_main.text(v['pos'], text, font=font, fill=v['font']['color'])
                f_name = f"{imageDict['name']}_{int(time.time())}.png"
                f_path = f"static/images/generated/"
                im.save(f_path+f_name)
                await loadingMessage.delete()
                await ctx.send(content=None, file=discord.File(f_path+f_name, filename=f_name))
                return
        else:
            await error.Error(self.bot, "Invalid image name", "The requested image is not available.").send(ctx)
            return
        
def setup(bot):
    bot.add_cog(Images(bot))