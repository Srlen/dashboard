import discord
from discord.ext.commands import Bot as BotBase
from discord.ext import ipc
from prisma import Prisma
# from dashboard import app
class MainBot(BotBase):
    # web = app
    prisma = Prisma()