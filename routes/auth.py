
from quart import Blueprint, redirect, url_for, render_template, current_app
from quart_discord import Unauthorized, requires_authorization

auth = Blueprint("auth", __name__)


@auth.route("/")
async def index():
    if not await current_app.discord.authorized:
        return await render_template("login.html", login=url_for(".login_with_data"))
    return redirect(url_for(".me"))


@auth.route("/login/")
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
    await current_app.ipc.request("auth_done", user_id=user.id)
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
