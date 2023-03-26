from discord.ext import commands
from discord import Embed, Activity, ActivityType
import json
from ...utilities import utils
from ...utilities import logger as log

class Debug(commands.Cog, name='Utilities'):
    """Provides useful utilities/debugging commands"""
    def __init__(self, bot):
        self.bot = bot

        config = json.load(open('config.json'))
        self.ownerNames = config['ownerNames']
        self.ownerIDs = config['ownerIDs']
        self.prefix = config['prefix']
        self.version = config['version']
        self.activity = config['activity']

    @commands.Cog.listener()
    async def on_ready(self):
        """Shows what servers the bot is in and confirms when bot comes online"""            
        member_count = 0
        guild_string = ""
        for g in self.bot.guilds:
            guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
            member_count += g.member_count

        log.logger.info(f"Bot '{self.bot.user.name}' has connected, active on {len(self.bot.guilds)} guilds:\n{guild_string}")

        await self.bot.change_presence(
            activity = Activity(type=ActivityType.watching, name=self.activity))

    @commands.command(
        help="Shows the ping/latency of the bot in milliseconds",
        brief="Shows ping"
    )
    async def ping(self, ctx):
        client = self.bot
        latency = round(client.latency * 1000)
        msg = f':ping_pong: The ping is **{latency}** ms!'

        if latency <= 50:
            embed=Embed(title="PING", description=msg, color=0x44ff44)
        elif latency <= 100:
            embed=Embed(title="PING", description=msg, color=0xffd000)
        elif latency <= 200:
            embed=Embed(title="PING", description=msg, color=0xff6600)
        else:
            embed=Embed(title="PING", description=msg, color=0x990000)
        
        await ctx.send(embed=embed)

    @commands.command(
        aliases=['h'],
        help="Shows this help menu",
        brief="Shows help"
    )
    async def help(self, ctx, *params):
        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not params:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owners = [ctx.guild.get_member(id).mention for id in self.ownerIDs]

            except AttributeError:
                owners = self.ownerNames

            # starting to build embed
            emb = Embed(
                title='Commands and modules',
                color=utils.blue_light,
                description=f'Use `{self.prefix}help <module>` to gain more information about a specific module\n'
            )

            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                # ignoring boring cogs
                if cog == "MessageListener" or cog == "Help":
                    continue
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating through uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(
                name="About",
                value=f"This bot is maintained by {', '.join(owners)}.\n"
            )
            emb.set_footer(text=f"Bot is running Version: {self.version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(params) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == params[0].lower():

                    # making title - getting description from doc-string below class
                    emb = Embed(
                        title=f'{cog} - commands',
                        description=self.bot.cogs[cog].__doc__,
                        color=utils.green
                    )

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"{self.prefix}{command.name}", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = Embed(
                    title="What's that?!",
                    description=f"I've never heard from a module called `{params[0]}` before :scream:",
                    color=utils.orange
                )

        # too many cogs requested - only one at a time allowed
        elif len(params) > 1:
            emb = Embed(
                title="That's too much.",
                description="Please request only one module at once :sweat_smile:",
                color=utils.orange
            )

        else:
            emb = Embed(
                title="It's a magical place.",
                description="I don't know how you got here. But I didn't see this coming at all.\n\
                    Please report this issue to a bot maintainer.",
                color=utils.orange)

        # sending reply embed using our own function defined above
        await utils.send_embed(ctx, emb)
