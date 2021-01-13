from abc import ABC, abstractmethod
from utils.scraper_utils import get_session, get_html
from bs4 import BeautifulSoup
from discord import Embed
import utils, time


class UpdateScraper(ABC):
	@classmethod
	async def get_updates(cls):
		session= get_session()

		updates= await cls.parse_update_page(session)
		async for x in (cls.filter_updates(updates, session)):
			yield cls.format_update(x)

		await session.close()

	@classmethod
	async def get_series_data(cls, update, session=None):
		# inits
		name= update['series']
		link= update['series_link']

		DATA= utils.load_json_with_default(utils.SERIES_CACHE, {})
		CONFIG= utils.load_bot_config()

		# refresh data if new series or not updated in a while
		if name in DATA:
			last_check= time.time() - DATA[name].get('last_checked', 0)

		if name not in DATA or last_check > CONFIG['series_refresh_rate']*24*60*60:
			# get data
			html= await get_html(link, session)
			soup= BeautifulSoup(html, 'html.parser')
			s_data= cls.parse_series_page(soup, update)
			s_data['link']= link

			# cache
			DATA[name]= s_data
			DATA[name]['last_checked']= time.time()
			utils.dump_json(DATA, utils.SERIES_CACHE)

		return DATA[name]


	@classmethod
	async def filter_updates(cls, updates, session=None):
		# inits
		ret= []
		SEEN= utils.load_json_with_default(utils.SEEN_CACHE, [])
		BLACKLIST= utils.load_yaml_with_default(utils.BLACKLIST_FILE, default=[])

		for x in updates:
			# inits
			series_data= await cls.get_series_data(x, session)
			x['series_data']= series_data

			# ignore already seen
			hash= x['series'] + "_" + str(x['chapter_number'])
			if hash in SEEN:
				continue
			SEEN.append(hash)

			# ignore blacklisted
			flag= False
			for y in BLACKLIST:
				flag= utils.contains_all(to_search=series_data['display_name'], to_find=y)
				flag|= utils.contains_all(to_search=series_data['group'], to_find=y)

				if flag:
					break

			if flag:
				continue


			# return
			yield x

			# clean up
			utils.dump_json(SEEN, utils.SEEN_CACHE)

	@classmethod
	def get_mentions(cls, update):
		mentions= utils.load_yaml_with_default(utils.MENTIONS_FILE)
		data= update['series_data']
		ret= []

		for x,y in mentions.items():
			if 	utils.contains_all(to_search=data['display_name'], to_find=x) or \
				utils.contains_all(to_search=data['group'], to_find=x) or \
				x.lower() == "all":

				if not isinstance(y, list):
					y= [y]

				for role_id in y:
					ret.append(f"<@&{role_id}>")

		return " ".join(ret)


	@classmethod
	@abstractmethod
	def format_update(cls, update):
		"""
		update is a list entry from parse_update_page()

		returns dictionary of kwargs to use for discord.abc.Messageable.send()

		(namely an entry for "content" (string) or "embed" (discord.Embed))
		"""
		STRINGS= utils.load_yaml_with_default(utils.UPDATE_STRINGS)

		ret= utils.render(STRINGS['update_embed'], update)
		ret= utils.load_yaml_from_string(ret, safe=True)
		ret= Embed.from_dict(ret)

		return dict(content=cls.get_mentions(update), embed=ret)

	@staticmethod
	@abstractmethod
	def parse_series_page(soup, update):
		"""
		soup is a bs4.BeautifulSoup instance constructed from html of the series page

		returns dictionary that looks like

		dict(
			cover_link= ...,
			display_name= ...,
			description= ...,
			group= ...,
			group_link= ...,
		)
		"""
		pass

	@classmethod
	@abstractmethod
	async def parse_update_page(cls, session):
		"""
		session is a aiohttp.Session instance

		returns list of dictionaries, where each dictionary looks like

		dict(
			series= ...,
			series_link= ...,
			chapter_name= ...,
			chapter_number= ...,
			link= ...
		)
		"""
		pass