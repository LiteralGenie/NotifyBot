from discord.ext import tasks, commands
from classes.scrapers import *
from utils.cog_utils.update_utils import update_check, handle_loop_error
from classes.log.logger import Logger


class UpdateCog(commands.Cog, Logger):
	def __init__(self, bot):
		commands.Cog.__init__(self)
		Logger.__init__(self, __name__)

		self.bot= bot
		self.check_times= {}
		self.iterations= {}

		self.error_channel= self.bot.get_channel(self.bot.config['error_channel'])

		tmp= lambda x: self.bot.get_channel(self.bot.config[x + '_channel'])
		self.secret_channel= tmp('secret')
		self.get_loop('secret', GenkanScraper('secret'), self.secret_channel).start()


	def get_loop(self, name, ScraperClass, out_channel):
		@handle_loop_error(self)
		@update_check(name, self)
		async def loop():
			async for x in (ScraperClass.get_updates()):
				await out_channel.send(**x)

		kwargs = {
            'seconds': 5, 'minutes': 0, 'hours': 0,
			'count': None,
			'reconnect': True,
			'loop': None
        }
		return tasks.Loop(loop, **kwargs)