from discord.ext import commands
from discord_components import Button, ButtonStyle, InteractionType

class invite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="invite")
    async def invite(self, ctx, user_id: int):

        user = ctx.author
        guild = ctx.guild

        channel = self.database.get(guild.id, user.id)

        if not channel:
            await ctx.send(f"You don't have a channel! How are we gonna invite someone to a channel that doesn't exist?")
            return
        try:
            user = self.bot.get_user(user_id)
            await user.send(
            f"Hello! {ctx.author.mention} has requested you to join them in their testing channel! Please click the appropriate button to respond!",
            components=[
                [
                    Button(style=ButtonStyle.green, label="Accept Invite"),
                    Button(style=ButtonStyle.red, label="Decline Invite"),
                ],
            ],
        )

        except Exception as e:
            await ctx.reply("Hmm, something went wrong! It's likely we couldn't find this user, or they have their DMs disabled!")

    @commands.Cog.listener()
    async def on_button_click(self, res):
        """
        Possible interaction types:
        - Pong
        - ChannelMessageWithSource
        - DeferredChannelMessageWithSource
        - DeferredUpdateMessage
        - UpdateMessage
        """

        await res.respond(
            type=InteractionType.ChannelMessageWithSource, content=f"{res.component.label} pressed"
        )

def setup(bot):
    bot.add_cog(invite(bot))