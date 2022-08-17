import asyncio
import os
from quart import Quart, redirect, url_for, current_app
from dotenv import load_dotenv
from routes.auth import auth
from routes.guilds import guilds
from routes.user import user
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
load_dotenv()
app = Quart(__name__)
app.secret_key = os.environ["SECRET_KEY"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.
app.config["DISCORD_CLIENT_ID"] = int(os.environ["DISCORD_CLIENT_ID"]) # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]          # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"       # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = os.environ["BOT_TOKEN"]      # Required to access BOT resources.
client = ipc.Client(host="127.0.0.1", port=8080, secret_key=os.environ["SECRET_KEY"])

@app.before_serving
async def create_session():
  current_app.discord =  DiscordOAuth2Session(app)
  current_app.client = client



app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(guilds, url_prefix="/")
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(client.start(loop=loop)) # `Client.start()` returns new Client instance or None if it fails to start
        app.run(use_reloader=True, port=5000, debug=True, loop=loop)
    finally:
        loop.run_until_complete(app.client.close()) # Closes the session, doesn't close the loop
        loop.close()