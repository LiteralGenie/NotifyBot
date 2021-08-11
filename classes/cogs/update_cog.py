import asyncio

from discord import Embed
from discord.ext import commands

import utils
from classes import AmyBotU, Update
from classes.scrapers import MadaraScraper
from classes.scrapers.arang import ArangScraper
from classes.scrapers.genkan import GenkanScraper
from classes.scrapers.lht import LhtScraper
from classes.scrapers.reaper import ReaperScraper
from classes.scrapers.update import UpdateScraper
from classes.state.scraper_config import ScraperConfig


class UpdateCog(commands.Cog):
	def __init__(self, bot: AmyBotU):
		commands.Cog.__init__(self)
		self.bot = bot

		self.start()

	# start scrapers
	def start(self):
		# inits
		defaults = self.bot.config.defaults
		session = self.bot.context.session
		scrapers = []

		# madara
		for scraper_dict in self.bot.config['madara']:
			cfg = ScraperConfig(defaults, scraper_dict)
			scrapers.append(MadaraScraper(config=cfg, session=session))

		# genkan
		for scraper_dict in self.bot.config['genkan']:
			cfg = ScraperConfig(defaults, scraper_dict)
			scrapers.append(GenkanScraper(config=cfg, session=session))

		# misc
		cfg = ScraperConfig(defaults, self.bot.config['misc']['reaper'])
		scrapers.append(ReaperScraper(config=cfg, session=session))

		cfg = ScraperConfig(defaults, self.bot.config['misc']['lht'])
		scrapers.append(LhtScraper(config=cfg, session=session))

		cfg = ScraperConfig(defaults, self.bot.config['misc']['arang'])
		scrapers.append(ArangScraper(config=cfg, session=session))

		# start
		for s in scrapers:
			asyncio.create_task(self._start_scraper(s))

	async def _start_scraper(self, scraper: UpdateScraper):
		out_channel = self.bot.get_channel(scraper.config.out)

		async for up in scraper.loop():
			# format
			mentions = self.get_mentions(up, scraper)
			msg = self.format_update(up, mentions)

			# send
			await out_channel.send(**msg)

			# sleep
			await asyncio.sleep(self.bot.config.msg_delay)

	def format_update(self, update: Update, mentions: list[str]):
		"""
		returns dictionary of kwargs to use for discord.abc.Messageable.send()
		(namely an entry for "content" (string) or "embed" (discord.Embed))
		"""
		STRINGS= utils.load_yaml_with_default(utils.UPDATE_STRINGS)

		embed= utils.render(STRINGS['series_update_embed'], update=update)
		embed= utils.load_yaml_from_string(embed, safe=True)

		content = " ".join(mentions)
		if "content" in embed:
			content+= "\n" + embed.get('content')
			del embed['content']

		return dict(content=content, embed=Embed.from_dict(embed))

	def get_mentions(self, update: Update, scraper: UpdateScraper) -> list[str]:
		pings = self.bot.config.global_pings.copy()
		pings += scraper.config.pings.copy()

		ret = [f"<@&{id}>" for id in pings]
		return ret