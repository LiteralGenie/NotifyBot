from mako.template import Template
from mako.lookup import TemplateLookup
from quart import Quart, Response
from discord.ext import ipc
import utils

from mako import exceptions


# load values
general= utils.load_bot_config()
roles= utils.load_yaml(utils.MENTIONS_FILE)

# render template
template_dir= utils.WEBVIEW_DIR + "settings/templates/"
lookup= TemplateLookup(directories=[template_dir])

template= Template(
	filename=template_dir + "index.html",
	lookup=lookup
)

# connect to bot
config= utils.load_bot_config()
ipc_client = ipc.Client(
    secret_key=config['ipc_key'],
    port=config['ipc_port']
)

# start web app
app= Quart(__name__)
@app.route("/")
async def index():
	roles_available= await ipc_client.request("get_available_roles")

	try:
		html= template.render(ROLES=roles, GENERAL=general,
							  ROLES_AVAILABLE=roles_available)
	except:
		return exceptions.html_error_template().render()

	return Response(html)

if __name__ == "__main__":
	app.run()