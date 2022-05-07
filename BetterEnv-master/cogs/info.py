from discord.ext import commands
import discord

description = ("Basically {}, this is a channel where you can test your bot, or get help with code! "
               "Left dormant for more than 30 days, it will be deleted. If you want to delete it use `be!close`.")

class info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="info")
    async def info(self, ctx):
        await ctx.reply("Command in development!")

    @commands.command(name="source", aliases=["src", "code", "github"])
    async def source(self, ctx):
        embed = discord.Embed(title=f"Wanna get involved with development?", description="Sure! [Here](https://github.com/Codeize/BetterEnv) is the link to the bot's source code!", color=0x80ff00)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Bot Developed By Codeize with Python. 😎")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))