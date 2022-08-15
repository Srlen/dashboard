from quart import Blueprint, redirect, url_for, render_template, current_app
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
user = Blueprint("user", __name__)
