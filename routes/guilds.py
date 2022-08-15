from quart import Blueprint, redirect, url_for, render_template, current_app
from quart_discord import Unauthorized, requires_authorization

guilds = Blueprint("guilds", __name__)

@guilds.route("/add_to/<int:guild_id>/")
@requires_authorization
async def add_to_guild(guild_id):
    user = await current_app.discord.fetch_user()
    return user.add_to_guild(guild_id)