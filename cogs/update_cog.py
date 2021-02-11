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


		# zzz, this was prettier before they requested separate channels
		tmp= lambda x: self.bot.get_channel(self.bot.config[x + '_channel'])
		self.ann_channel= tmp('ann')
		self.levi_channel= tmp('levi')
		self.sushi_channel= tmp('sushi')
		self.md_channel= tmp('md')
		self.lht_channel= tmp('lht')
		self.sks_channel= tmp('sks')
		self.reaper_channel= tmp('reaper')
		self.noname_channel= tmp('noname')

		self.get_loop('sks', GenkanScraper('sks'), self.sks_channel).start()
		self.get_loop('levi', GenkanScraper('levi'), self.levi_channel).start()
		self.get_loop('reaper', GenkanScraper('reaper'), self.reaper_channel).start()
		self.get_loop('noname', GenkanScraper('noname'), self.noname_channel).start()

		# self.get_loop('sushi', SushiScraper(), self.sushi_channel).start()
		# self.get_loop('md', MdScraper(), self.md_channel).start()
		# self.get_loop('ann', AnnScraper(), self.ann_channel).start()
		# self.get_loop('lht', LhtScraper(), self.lht_channel).start()


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