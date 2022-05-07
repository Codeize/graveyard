from discord.ext import commands
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

description = ("Basically {}, this is a channel where you can test your bot, or get help with code! "
               "Left dormant for more than 30 days, it will be deleted. If you want to delete it use `be!close`.")

class new(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="new")
    async def new(self, ctx, name: str, id: int):

        user = ctx.author
        guild = ctx.guild

        channel = self.database.get(guild.id, user.id)
        if channel:
            await ctx.send(f"Hmm, it seems you already have a testing channel, <#{channel}>")
            return

        if name or id:

            category = discord.utils.get(guild.categories, name="secure testing")
            if not category:
                category = await guild.create_category("secure testing")

            logs = discord.utils.get(guild.channels, name=f"channel-logs")
            if not logs:
                logs = await guild.create_text_channel(f"channel-logs", category=category, position=0)

            link = f"https://discord.com/oauth2/authorize?client_id={id}&guild_id={ctx.guild.id}&scope=bot"
            embed = discord.Embed(title="New Bot Added!", description=f"{ctx.author.mention} - {ctx.author.id} | Has requested a bot to be added! Click the button below to authorize it! (Bot has no additional Discord permissions)")
            await logs.send(embed=embed)
            await logs.send(
            "Here is the new invite url",
            components=[
                Button(style=ButtonStyle.URL, label="URL", url=link),
            ],
        )

            channel = await guild.create_text_channel(f"{name}-testing", category=category)
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            self.database.add(guild.id, channel.id, user.id)

            embed = discord.Embed(title=f"Welcome to {name}-testing!", description=description.format(user.mention), color=0x80ff00)
            embed.set_author(name=user, icon_url=user.avatar_url)
            embed.set_footer(text="Bot Developed By Codeize with Python. 😎")

            message = await channel.send(embed=embed)
            # await channel.send("Please submit your bot to be added via its ID: `be!request <botID>`!")
            await message.pin()

            await ctx.send(f"{user.mention}, created <#{channel.id}> successfully. Enjoy!")
            await logs.send(f"{user.mention} - (`{user.id}`) | Created a testing channel")

        else:
            await ctx.reply("Nope, try again but this time actually provide the bot's name!")

def setup(bot):
    bot.add_cog(new(bot))