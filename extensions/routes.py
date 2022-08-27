import os
import sys
import logging
import discord
from discord.ext import commands, ipc
from discord.ext.ipc.server import Server
from discord.ext.ipc.errors import IPCError
from discord.ext.ipc.objects import ClientPayload
class Routes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, standard_port=4000, secret_key=os.environ["SECRET_KEY"], do_multicast=False)

    async def cog_load(self) -> None:
        await self.bot.ipc.start()

    async def cog_unload(self) -> None:
        await self.bot.ipc.stop()
        self.bot.ipc = None

    @commands.Cog.listener()
    async def on_ipc_ready(self):
        logging.info("Ipc is ready")
    
    @commands.Cog.listener()
    async def on_ipc_error(self, endpoint: str, error: IPCError):
        logging.error(endpoint, "raised", error, file=sys.stderr)
    
    @Server.route()
    async def auth_done(self, data):
        user = await self.bot.fetch_user(data.user_id)
        await user.send(embed=discord.Embed(description="Done you make an connections with me!", title="done!", colour=discord.Colour.green()))
        return user._to_minimal_user_json() # THE OUTPUT MUST BE JSON SERIALIZABLE!

async def setup(bot):
    await bot.add_cog(Routes(bot))