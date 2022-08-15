import os
from typing import List
from flask import Flask, redirect, url_for, render_template, current_app
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from dotenv import load_dotenv
from routes.auth import auth
from routes.guilds import guilds
from routes.user import user
# load_dotenv()
# app = Flask(__name__)

# app.secret_key = b"423423"
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

# app.config["DISCORD_CLIENT_ID"] = 993309758780100648    # Discord client ID.
# app.config["DISCORD_CLIENT_SECRET"] = "oYfulsngiTt9vQuTFXCjHy8At1to9B3v"                # Discord client secret.
# app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"                 # URL to your callback endpoint.
# app.config["DISCORD_BOT_TOKEN"] = os.environ["BOT_TOKEN"]                    # Required to access BOT resources.
# discord = DiscordOAuth2Session()
# app.register_blueprint(auth, url_prefix="/")
# app.register_blueprint(user, url_prefix="/")
# app.register_blueprint(guilds, url_prefix="/")
def web(app: Flask,secret_key: str):
    app.secret_key = secret_key
    return app