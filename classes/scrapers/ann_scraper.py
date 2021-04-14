from bs4 import BeautifulSoup
from utils.scraper_utils import get_session, get_html
from discord import Embed
import utils, asyncio


# @todo: create superclass for AnnScraper and UpdateScraper
class AnnScraper:
	@classmethod
	def format_update(cls, update):
		STRINGS= utils.load_yaml_with_default(utils.UPDATE_STRINGS)

		ret= utils.render(STRINGS['news_update_embed'], update)
		ret= utils.load_yaml_from_string(ret, safe=True)
		ret= Embed.from_dict(ret)

		return dict(content=cls.get_mentions(), embed=ret)

	@staticmethod
	def get_mentions():
		mentions= utils.load_yaml_with_default(utils.MENTIONS_FILE)
		name= "ann https://www.animenewsnetwork.com/ anime news network"
		ret= []

		for x,y in mentions.items():
			x= [y.strip() for y in x.split(",")]
			if 	utils.contains_all(to_search=name, to_find=x) or \
				x.lower() == "all":

				if not isinstance(y, list):
					y= [y]

				for role_id in y:
					ret.append(f"<@&{role_id}>")

		return " ".join(ret)

	@staticmethod
	def filter_updates(updates):
		# inits
		SEEN= utils.load_json_with_default(utils.SEEN_CACHE, [])

		for x in updates:
			# check if seen
			hash= x['title'].replace(" ","-")
			if hash in SEEN:
				continue
			SEEN.append(hash)

			# return
			yield x

			# clean up
			SEEN= SEEN[-12345:]
			utils.dump_json(SEEN, utils.SEEN_CACHE)

	@classmethod
	async def get_updates(cls):
		session= get_session()

		lst= await cls.fetch_updates(session)
		lst= cls.filter_updates(lst)

		for x in lst:
			x['cover_link']= await cls.get_cover_link(x, session)
			yield cls.format_update(x)
			await asyncio.sleep(3)

		await session.close()


	@classmethod
	async def fetch_updates(cls, session=None):
		# inits
		ret= []
		CONFIG= utils.load_bot_config()

		# get rss feed
		xml= await get_html(CONFIG['ann_update_link'], session)
		soup= BeautifulSoup(xml, 'lxml')

		# parse items
		items= soup.find_all('item')
		for it in items:
			title= it.find('title').get_text()
			link= it.find('guid').get_text()
			description= it.find('description').get_text()

			ret.append(dict(
				title=title,
				link=link,
				description=description
			))

		return ret

	@staticmethod
	async def get_cover_link(update, session):
		cover_html= await get_html(update['link'], session)
		cover_soup= BeautifulSoup(cover_html, 'html.parser')
		cover_link= cover_soup.find(class_="fright lazyload")
		if cover_link:
			cover_link= "https://www.animenewsnetwork.com" + cover_link['data-src']
		else:
			cover_link= ""

		return cover_link