from flask import Blueprint, redirect, url_for, render_template, current_app
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
user = Blueprint("user", __name__)

@user.route("/me/")
async def me():
    user = current_app.discord.discord.fetch_user()
    guilds = current_app.discord.fetch_guilds()
    return render_template("user.html", user=user, logout=url_for(".logout"), guilds=guilds)
