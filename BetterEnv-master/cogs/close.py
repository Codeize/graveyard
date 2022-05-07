from discord.ext import commands
import discord

class close(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="close")
    async def close(self, ctx):

        user = ctx.author
        guild = ctx.guild

        channel = self.database.get(guild.id, user.id)
        if not channel:
            await ctx.send(f"Hmm, it seems you don't have a testing channel")
            return

        await guild.get_channel(channel).delete()
        self.database.remove(guild.id, user.id)

        category = discord.utils.get(guild.categories, name="secure testing")
        if not category:
            category = await guild.create_category("secure testing")

        logs = discord.utils.get(guild.channels, name=f"channel-logs")
        if not logs:
            logs = await guild.create_text_channel(f"channel-logs", category=category, position=0)

        if ctx.channel.id != channel:
            await ctx.channel.send("Deleted your testing channel")
        await logs.send(f"{user.mention} - (`{user.id}`) | Deleted a testing channel")

def setup(bot):
    bot.add_cog(close(bot))