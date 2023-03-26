from discord.ext import commands
import discord
import sqlite3
import sys
from ...utilities import utils
from ...utilities import logger as log

class Currency(commands.Cog, name='Currency'):
    """Provides commands related to the server currency"""
    def __init__(self, bot):
        self.bot = bot
        self.conn = None

    @commands.Cog.listener()
    async def on_ready(self):
        """Open connection to DB"""            
        try:
            self.conn = sqlite3.connect('./data/currency.db')
            log.logger.info('Opened Currency Database.')
        except sqlite3.Error as e:
            log.logger.critical(f'Failed to open Currency Database: {e}')
            sys.exit()

    @commands.command(
        help="Allow GOSHO Bot to start tracking your server currency.",
        brief="Start tracking currency."
    )
    async def track_currency(self, ctx: commands.Context):
        server = ctx.guild.id
        user = ctx.author.id
        
        users = self.execute_query('''
            SELECT DiscordId
            FROM Users
            WHERE ServerId = ?
            AND DiscordId = ?
        ''', (server, user))

        if user not in users:
            self.execute_query('''
                INSERT INTO Users(ServerId, DiscordId)
                VALUES(?,?)
            ''', (server, user))

            user_id = self.execute_query('''
                SELECT Id
                FROM Users
                WHERE ServerId = ?
                AND DiscordId = ?
            ''', (server, user))[0][0]

            self.execute_query('''
                INSERT INTO Balance(Id, Balance)
                VALUES(?, 100)
            ''', (user_id,))

            self.execute_query('''
                INSERT INTO TransactionLog(Id, Description, Change)
                VALUES(?, 'Initial Balance', 100)
            ''', (user_id,))
            
            self.commit_changes()

            await ctx.send(content='Now tracking your currency.')
        else:
            await ctx.send(content='You are already being tracked!')

    @commands.command(
        help="Shows currency of members in server.",
        brief="Shows currency"
    )
    async def currency(self, ctx: commands.Context):
        data = self.execute_query('''
            SELECT U.DiscordId, B.Balance
            FROM Users U
            INNER JOIN Balance B
                ON B.Id = U.Id
            WHERE U.ServerId = ?
        ''', (ctx.guild.id,))

        msg = ''
        for user in data:
            msg = msg + f'<@!{user[0]}>:\t{user[1]} tokens\n'

        await ctx.send(embed=utils.make_embed(title='Currency', color=discord.Color.from_rgb(133, 187, 101), value=msg))

    # ------------------------------------------------------------------------ #
    # Helper methods
    def execute_query(self, exec_sql, params = None) -> list:
        """
        Execute a query from the exec_sql statement
        @param exec_sql an exec statement
        @param params list of params for the exec statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(exec_sql, params)

            return c.fetchall()
        except sqlite3.Error as e:
            log.logger.error(f'SQL Query Failed: {exec_sql}: {e}')
    
    def commit_changes(self):
        """
        Commit all changes made
        :return:
        """
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            log.logger.error(f'SQL Commit Failed: {e}')