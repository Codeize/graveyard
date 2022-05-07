from discord.ext import commands
import discord

class setup_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="setup")
    async def new(self, ctx):

        category = discord.utils.get(ctx.guild.categories, name="Secure Testing")
        if not category:
            category = await ctx.guild.create_category("Secure Testing")

        logs = discord.utils.get(ctx.guild.channels, name=f"channel-logs")
        if not logs:
            logs = await ctx.guild.create_text_channel(f"channel-logs", category=category, position=0)

        channel = await ctx.guild.create_text_channel(f"make-channel", category=category)

        await ctx.message.add_reaction('✔️')
        await ctx.reply("Done! You now have a new category named Secure Testing, along with #channel-logs, a make channel VC and #make-channel ! Please don't change the name or the category or channels. This will cause the bot to overwrite the current setup and re-issue all channels.")

def setup(bot):
    bot.add_cog(setup_cog(bot))