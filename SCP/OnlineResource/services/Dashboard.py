from ssl import match_hostname
from quart import Quart, render_template, request, session, redirect, url_for
from oath import Oauth
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc

ipc_client = ipc.Client(secret_key="g")

app = Quart(
    __name__, 
    template_folder=r"C:\Users\trexx\Documents\PYTHON CODE LOL\SCP-16-Tsundere-Discord-Bot\SCP\OnlineResource\templates",
    static_folder=r"C:\Users\trexx\Documents\PYTHON CODE LOL\SCP-16-Tsundere-Discord-Bot\SCP\OnlineResource\static",
    )
app.config["SECRET_KEY"] = "geneavianina"
app.config["DISCORD_CLIENT_ID"] = 822265614244511754   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "vaqJa9ZQAWawL7FJlHYYBeuQw-JIBtO2"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"   

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    guild_count = await ipc_client.request("get_guild_count")
    return await render_template(
        "./intex.html", 
        discord_url=Oauth.discord_login_url, 
        authorized = await discord.authorized,
        servercount=guild_count)

@app.route("/intex.html")
async def home1():
    guild_count = await ipc_client.request("get_guild_count")

    return await render_template(
        "./intex.html", 
        discord_url=Oauth.discord_login_url,
        authorized = await discord.authorized, 
        servercount=guild_count)


@app.route("/About.html")
async def about():
    return await render_template("./About.html", discord_url=Oauth.discord_login_url, authorized = await discord.authorized)

@app.route("/dashboard/<int:guild_id>")
async def dashboard(guild_id):
	if not await discord.authorized:
		return redirect(url_for("login")) 
	guild = await ipc_client.request("get_guild", guild_id = guild_id)
	if guild is None:
		return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
	return guild["name"]

@app.route("/selectServerPage.html")
async def selectServer():
    if not await discord.authorized:
        return redirect(url_for("login")) 

    guild_count = await ipc_client.request("get_guild_count")
    guild_ids = await ipc_client.request("get_guild_ids")

    user_guilds = await discord.fetch_guilds()

    guilds = []

    for guild in user_guilds:
        if guild.permissions.administrator:			
            guild.class_color = "green-border" if guild.id in guild_ids else "red-border"
            guilds.append(guild)

    guilds.sort(key = lambda x: x.class_color == "red-border")
    name = (await discord.fetch_user()).name
    return await render_template("/selectServerPage.html", guild_count = guild_count, guilds = guilds, username=name)


@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    user = await discord.fetch_user()
    return await selectServer()


if __name__ == '__main__':
    app.run(debug=True)
