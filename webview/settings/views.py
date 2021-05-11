from quart import views, Response, request
from mako.template import Template
from webview import IPC_CLIENT
from . import LOOKUP, TEMPLATE_DIR
from ruamel.yaml import YAML
import utils, json


# GET for settings summary
class SettingsView(views.MethodView):
	async def get(self):
		bot_config= utils.load_bot_config()
		role_config= utils.load_yaml(utils.MENTIONS_FILE)

		roles_available= await IPC_CLIENT.request("get_available_roles")
		series_data= utils.load_json_with_default(utils.SERIES_CACHE, {})

		html= Template(filename=TEMPLATE_DIR + "index.html", lookup=LOOKUP).render(
			GENERAL=bot_config, ROLES=role_config,
		  	ROLES_AVAILABLE=roles_available, SERIES_DATA=series_data,
		)

		return Response(html)

# POST for bot config update
class GeneralView(views.MethodView):
	async def post(self):
		pass

# POST for ping-role update
class RoleView(views.MethodView):
	async def post(self):
		with open(utils.MENTIONS_FILE, "w") as file:
			data= await request.json
			print(data)
			YAML().dump(await request.json, file)

		msg= f"Role pings updated."
		msg+= f"\n```json\n{json.dumps(data,indent=2)}```"
		resp= await IPC_CLIENT.request("notify_role_update", msg=msg)
		print(resp)
		return ""