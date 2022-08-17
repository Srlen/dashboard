import os
import discord
from discord.ext.commands import Bot as BotBase
from prisma import Prisma
from discord.ext import ipc
# from dashboard import app
class MainBot(BotBase):
    # web = app
    prisma = Prisma()
    async def setup_hook(self) -> None:

        for extension in os.listdir("extensions/"):
            if extension.endswith(".py"):
                await self.load_extension(f"extensions.{extension[:-3]}")