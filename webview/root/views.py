from quart import redirect, url_for


async def home():
	return redirect(url_for("settings.index"))