from discord.ext import commands, tasks
import discord

from classes.state.bot_config import BotConfig
from classes.errors import ErrorHandler
from classes.state.bot_context import BotContext


# @TODO: logging
class AmyBotU(commands.Bot, ErrorHandler):
	def __init__(self, *args, **kwargs):
		# intents
		intents= discord.Intents.default()
		intents.guilds= True

		# init
		self.context = BotContext()
		self.config= self.context.config
		super().__init__(command_prefix=self.config['prefix'], intents=intents, *args, **kwargs)

	async def on_ready(self):
		print(f"Logged in as {self.user.display_name}#{self.user.discriminator}")

		# add cogs
		from classes.cogs import UpdateCog
		self.add_cog(UpdateCog(self))

	def start_bot(self):
		self.run(self.config['discord_key'])

	@tasks.loop(seconds=60)
	async def reload(self):
		self.config.load()