import logging
import os
import discord
import sys

from quart import Blueprint, redirect, url_for, render_template, current_app
from quart_discord import Unauthorized, requires_authorization

from discord.ext import commands, ipc

# class Routes(commands.Cog):
#     """"""
#     def __init__(self, bot):
#         self.bot = bot
#         if not hasattr(bot, "ipc"):
#             bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=5000, secret_key="your_secret_key_here")
#             bot.ipc.start()
#         @commands.Cog.listener()
#         async def on_ipc_ready(self):
#          logging.info("Ipc is ready")
    
#         @commands.Cog.listener()
#         async def on_ipc_error(self, endpoint: str, error: IPCError):
#           logging.error(endpoint, "raised", error, file=sys.stderr)
        
#         @route()
#         async def get_user_data(self, data):
#          user = self.bot.get_user(data.user_id)
#          return user._to_minimal_user_json() # THE OUTPUT MUST BE JSON SERIALIZABLE!

# async def setup(bot):
#     await bot.add_cog(Routes(bot))


auth = Blueprint("auth", __name__)
@auth.route("/")
async def index():
    if not await current_app.discord.authorized:
        return await render_template("login.html", login=url_for(".login_with_data"))
    return redirect(url_for(".me"))


@auth.route("/login-data/")
async def login_with_data():
    return await current_app.discord.create_session()

@auth.route("/logout/")
@requires_authorization
async def logout():
    current_app.discord.revoke()
    return redirect("http://127.0.0.1:5000/")

@auth.route("/callback/")
async def callback():
    await current_app.discord.callback()
    user = await current_app.discord.fetch_user()
    await current_app.client.request("auth_done", user_id=user.id)
    return redirect(url_for(".me"))

@auth.route("/me/")
@requires_authorization
async def me():
    user = await current_app.discord.fetch_user()
    guilds = await current_app.discord.fetch_guilds()
    return await render_template("user.html", user=user, logout=url_for(".logout"), guilds=guilds)


@auth.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect("http://127.0.0.1:5000/")