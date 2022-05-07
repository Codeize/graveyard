from discord.ext import commands
from discord_components import Button, ButtonStyle, InteractionType

class lockdown(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="lockdown")
    async def lockdown(self, ctx):

        user = ctx.author
        guild = ctx.guild

        channels = self.database.get_all(guild.id)
        for channel, b in channels:
            try:
                print(channel, b)
                await channel.send("hey")
            except Exception as e:
                await ctx.send("nope")
                print(e)
            
        

        

def setup(bot):
    bot.add_cog(lockdown(bot))