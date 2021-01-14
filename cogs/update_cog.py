from discord.ext import tasks, commands
from classes.scrapers import SushiScraper, LeviScraper, MdScraper
from utils.cog_utils.update_utils import update_check, handle_loop_error
from classes.log.logger import Logger
import asyncio, traceback, utils


class UpdateCog(commands.Cog, Logger):
	def __init__(self, bot):
		commands.Cog.__init__(self)
		Logger.__init__(self, __name__)

		self.bot= bot
		self.check_times= {}
		self.iterations= {}

		self.update_channel= self.bot.get_channel(self.bot.config['update_channel'])
		self.error_channel= self.bot.get_channel(self.bot.config['error_channel'])

		self.get_loop('sushi', SushiScraper).start()
		self.get_loop('levi', LeviScraper).start()
		self.get_loop('md', MdScraper).start()

	def get_loop(self, name, ScraperClass):
		@handle_loop_error(self)
		@update_check(name, self)
		async def loop():
			async for x in (ScraperClass.get_updates()):
				await self.update_channel.send(**x)

		kwargs = {
            'seconds': 5, 'minutes': 0, 'hours': 0,
			'count': None,
			'reconnect': True,
			'loop': None
        }
		return tasks.Loop(loop, **kwargs)