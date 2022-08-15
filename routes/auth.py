from flask import Blueprint, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask import current_app
auth = Blueprint("auth", __name__)
async def welcome_user(user):
    dm_channel = current_app.discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return current_app.discord.bot_request(
     f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"})


@auth.route("/")
async def index():
    if not current_app.discord.authorized:
        return render_template("login.html", login=url_for(".login_with_data"))
    return redirect(url_for(".me"))


@auth.route("/login-data/")
async def login_with_data():
    return current_app.discord.create_session(data=dict(redirect="/me/", coupon="15off", number=15, zero=0, status=False))

@auth.route("/logout/")
async def logout():
    current_app.discord.revoke()
    return redirect("http://127.0.0.1:5000/")

@auth.route("/me/")
async def me():
    user = current_app.discord.fetch_user()
    guilds = current_app.discord.fetch_guilds()
    return render_template("user.html", user=user, logout=url_for(".logout"), guilds=guilds)


@auth.route("/callback/")
async def callback():
    data = current_app.discord.callback()
    redirect_to = data.get("redirect", "/")

    user = current_app.discord.fetch_user()
    await welcome_user(user)

    return redirect(redirect_to)


@auth.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for(".login_with_data"))