import asyncio
import os
import discord
from discord.ext import commands
import json
from src.bot.cogs.debug import Debug
from src.bot.cogs.currency import Currency

secrets = json.load(open('secrets.json'))
config = json.load(open('config.json'))

async def load_cogs(bot: commands.Bot):
    await bot.add_cog(Debug(bot))
    await bot.add_cog(Currency(bot))

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    # Initialize the bot
    bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
    
    # Remove help command as we have a custom one
    bot.remove_command('help')

    # Load cogs
    asyncio.run(load_cogs(bot))
    
    # Run the bot
    bot.run(secrets['token'])