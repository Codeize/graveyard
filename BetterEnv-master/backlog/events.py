from discord.ext import commands
from discord import Embed

class joinleave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.serverlogs = self.bot.get_channel(827596867789520936)

    @commands.Cog.listener()
    async def on_guild_join(self, newguild):

        memcount = newguild.member_count
        embed = Embed(title=f"**Added** to `{newguild}`", description=str(newguild.id), color=self.bot.s_colour)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, oldguild):
        # TODO some sort of guild channel remove function

        memcount = oldguild.member_count
        embed = Embed(title=f"**Added** to `{oldguild}`", description=str(oldguild.id), color=self.bot.e_colour)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

def setup(bot):
    bot.add_cog(joinleave(bot))