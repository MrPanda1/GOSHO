from discord.ext import commands
import discord
from ...utilities import utils

class Currency(commands.Cog, name='Currency'):
    """Provides commands related to the server currency"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Shows currency of members in server. Specify a name or page number to filter results.",
        brief="Shows currency"
    )
    async def currency(self, ctx):
        data = [('<@!182711856975183872>', 150), ('<@!182711856975183872>', 200)]

        msg = ''
        for user in data:
            msg = msg + f'{user[0]}:\t{user[1]} tokens\n'

        await ctx.send(embed=utils.make_embed(title='Currency', color=discord.Color.from_rgb(133, 187, 101), value=msg))
