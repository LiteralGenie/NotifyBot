from discord.ext import tasks, commands
from classes.scrapers import SushiScraper
from utils.cog_utils.update_utils import update_check
import asyncio, time


class UpdateCog(commands.Cog):
	def __init__(self, bot):
		super().__init__()

		self.bot= bot
		self.check_times= {}
		self.iterations= {}

		self.check_sushi.start()

	@tasks.loop(minutes=1)
	@update_check('sushi')
	async def check_sushi(self):
		async for x in (SushiScraper.get_updates()):
			update_channel= self.bot.get_channel(self.bot.config['update_channel'])
			await update_channel.send(**x)
			await asyncio.sleep(self.bot.config['discord_message_delay'])
