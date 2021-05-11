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


		# todo: condense
		tmp= lambda x: self.bot.get_channel(self.bot.config[x + '_channel'])

		self.get_loop('sks', MadaraScraper('sks'), tmp('sks')).start()
		self.get_loop('levi', MadaraScraper('levi'), tmp('levi')).start()
		self.get_loop('arang', MadaraScraper('arang'), tmp('arang')).start()
		self.get_loop('tritinia', MadaraScraper('tritinia'), tmp('tritinia')).start()

		self.get_loop('reaper', GenkanScraper('reaper'), tmp('reaper')).start()
		self.get_loop('noname', GenkanScraper('noname'), tmp('noname')).start()

		self.get_loop('sushi', SushiScraper(), tmp('sushi')).start()
		self.get_loop('md', MdScraper(), tmp('md')).start()
		self.get_loop('ann', AnnScraper(), tmp('ann')).start()
		self.get_loop('lht', LhtScraper(), tmp('lht')).start()
		self.get_loop('flame', FlameScraper(), tmp('flame')).start()


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