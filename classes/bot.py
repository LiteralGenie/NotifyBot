from discord.ext import commands, ipc
from classes.errors import ErrorHandler
import discord, utils


# @TODO: logging
class AmyBotU(commands.Bot, ErrorHandler):
	def __init__(self, *args, **kwargs):
		# intents
		intents= discord.Intents.default()
		intents.guilds= True

		# init
		self.config= utils.load_bot_config()
		super().__init__(command_prefix=self.config['prefix'], intents=intents, *args, **kwargs)

		# ipc server for web requests
		self.ipc_server = ipc.Server(self, secret_key=self.config['ipc_key'], port=self.config['ipc_port'])

	async def on_ready(self):
		print(f"Logged in as {self.user.display_name}#{self.user.discriminator}")

		# add cogs
		from classes.cogs import UpdateCog, WebviewCog
		self.add_cog(UpdateCog(self))
		self.add_cog(WebviewCog(self))

	def start_bot(self):
		self.ipc_server.start()
		self.run(self.config['discord_key'])