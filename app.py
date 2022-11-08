import os
from quart import Quart
from dotenv import load_dotenv
from routes.auth import auth
from routes.guilds import guilds
from routes.user import user
from quart_discord import DiscordOAuth2Session
from discord.ext.ipc import Client
load_dotenv()
app = Quart(__name__)

app.secret_key = os.environ["SECRET_KEY"]
# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
# Discord client ID.
app.config["DISCORD_CLIENT_ID"] = int(os.environ["DISCORD_CLIENT_ID"])
# Discord client secret.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
# URL to your callback endpoint.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback/"
# Required to access BOT resources.
app.config["DISCORD_BOT_TOKEN"] = os.environ["BOT_TOKEN"]
discord = DiscordOAuth2Session(app)
app.ipc = Client(secret_key=os.environ["SECRET_KEY"], do_multicast=False)
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(guilds, url_prefix="/")

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True, port=5000)
