from discord.ext import tasks, commands
from classes.scrapers import SushiScraper, LeviScraper, MdScraper
from utils.cog_utils.update_utils import update_check
import asyncio


class UpdateCog(commands.Cog):
	def __init__(self, bot):
		super().__init__()

		self.bot= bot
		self.check_times= {}
		self.iterations= {}

		self.check_sushi.start()
		self.check_levi.start()
		self.check_md.start()

	@tasks.loop(seconds=5)
	@update_check('sushi')
	async def check_sushi(self):
		async for x in (SushiScraper.get_updates()):
			update_channel= self.bot.get_channel(self.bot.config['update_channel'])
			await update_channel.send(**x)
			await asyncio.sleep(self.bot.config['discord_message_delay'])


	@tasks.loop(seconds=5)
	@update_check('levi')
	async def check_levi(self):
		async for x in (LeviScraper.get_updates()):
			update_channel= self.bot.get_channel(self.bot.config['update_channel'])
			await update_channel.send(**x)
			await asyncio.sleep(self.bot.config['discord_message_delay'])

	@tasks.loop(seconds=5)
	@update_check('md')
	async def check_md(self):
		async for x in (MdScraper.get_updates()):
			update_channel= self.bot.get_channel(self.bot.config['update_channel'])
			await update_channel.send(**x)
			await asyncio.sleep(self.bot.config['discord_message_delay'])