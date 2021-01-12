from discord.ext import commands
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

	async def on_ready(self):
		print(f"Logged in as {self.user.display_name}#{self.user.discriminator}")

		# add cogs
		from cogs import UpdateCog
		self.add_cog(UpdateCog(self))
