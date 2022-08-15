from flask import Blueprint, redirect, url_for, render_template, current_app
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

guilds = Blueprint("guilds", __name__)
@guilds.route("/add_to/<int:guild_id>/")
async def add_to_guild(guild_id):
    user = current_app.discord.fetch_user()
    return user.add_to_guild(guild_id)