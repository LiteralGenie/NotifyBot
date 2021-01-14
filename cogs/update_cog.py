from discord.ext import tasks, commands
from classes.scrapers import SushiScraper, LeviScraper, MdScraper, AnnScraper
from utils.cog_utils.update_utils import update_check, handle_loop_error
from classes.log.logger import Logger


class UpdateCog(commands.Cog, Logger):
	def __init__(self, bot):
		commands.Cog.__init__(self)
		Logger.__init__(self, __name__)

		self.bot= bot
		self.check_times= {}
		self.iterations= {}

		self.news_channel= self.bot.get_channel(self.bot.config['news_channel'])
		self.series_channel= self.bot.get_channel(self.bot.config['series_channel'])
		self.error_channel= self.bot.get_channel(self.bot.config['error_channel'])

		self.get_loop('sushi', SushiScraper).start()
		self.get_loop('levi', LeviScraper).start()
		self.get_loop('md', MdScraper).start()
		self.get_loop('ann', AnnScraper, channel=self.news_channel).start()

	def get_loop(self, name, ScraperClass, channel=None):
		if channel is None:
			channel= self.series_channel

		@handle_loop_error(self)
		@update_check(name, self)
		async def loop():
			async for x in (ScraperClass.get_updates()):
				await channel.send(**x)

		kwargs = {
            'seconds': 5, 'minutes': 0, 'hours': 0,
			'count': None,
			'reconnect': True,
			'loop': None
        }
		return tasks.Loop(loop, **kwargs)