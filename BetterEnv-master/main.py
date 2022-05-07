import os
import json

from discord_components import DiscordComponents, Button

from discord.ext import commands
import discord

import utils.utils as utils

owners = [668423998777982997, 671791003065384987]
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="be!", owner_ids=owners, intents=intents)
bot.remove_command("help")
bot.database = utils.database()

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")

bot.e_colour = 0xff0000
bot.s_colour = 0x31e30e

@bot.event
async def on_ready():

    print(f"We have logged in as {bot.user}")

    Activity = discord.Activity
    watching = discord.ActivityType.watching
    DiscordComponents(bot)
    await bot.change_presence(activity=Activity(type=watching, name=f";)"))

    print(discord.__version__)

@bot.event
async def on_command_error(ctx, error):

    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):

        m, s = [int(i) for i in divmod(error.retry_after, 60)]
        h, m = [int(i) for i in divmod(m, 60)]

        if not h and not m:
            await ctx.send(f' You must wait {s}s to use this command!')

        elif not h:
            await ctx.send(f' You must wait {m}m and {s}s to use this command!')

        else:
            await ctx.send(f' You must wait {h}h, {m}m and {s}s to use this command!')

    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command.")

    raise error

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    content = message.content
    mention = f"<@!{bot.user.id}>"

    bot.database.interact(message.channel.id)

    if content.startswith(mention) and len(content) == len(mention):
        await message.channel.send(f"My prefix here is be!", delete_after=15)

    await bot.process_commands(message)

with open("configuration.json", "r") as config:
    data = json.load(config)

bot.run(data["token"])