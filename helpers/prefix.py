import discord
from discord.ext import commands

async def prefix_bot(bot: commands.Bot, message: discord.Message):
    return "!"