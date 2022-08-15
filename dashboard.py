import os
from flask import Flask
from dotenv import load_dotenv
from routes import web
from routes.auth import auth
from routes.guilds import guilds
from routes.user import user
from flask_discord import DiscordOAuth2Session
load_dotenv()
app = web(
    Flask(__name__),
    "srlen-server"
    )

app.secret_key = os.environ["SECRET_KEY"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.
app.config["DISCORD_CLIENT_ID"] = int(os.environ["DISCORD_CLIENT_ID"]) # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]          # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"       # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = os.environ["BOT_TOKEN"]      # Required to access BOT resources.
discord = DiscordOAuth2Session(app)
    
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(guilds, url_prefix="/")

app.run(debug=True, port=5000)