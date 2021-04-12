from quart import Quart, Response
from discord.ext import ipc
import utils

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
	import time
	ping_time= await ipc_client.request('ping')
	ping_time= time.time_ns() - ping_time
	content= f"Pong in {ping_time / 10**6:.1f} ms!"

	return Response(f"""<html>
	<head></head>
	</body><p>{content}</p></body>
	</html>""")

if __name__ == "__main__":
	app.run()