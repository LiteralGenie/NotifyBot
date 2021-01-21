from utils.scraper_utils import get_html, get_session
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils, time


class GenkanScraper(UpdateScraper):
	def __init__(self, key):
		CONFIG= utils.load_bot_config()
		self.home_link= CONFIG[key + '_home_link']
		self.name= CONFIG[key + '_name']
		self.update_link= f"{self.home_link}/latest"

	async def get_updates(self):
		session= get_session()

		updates= await self.parse_update_page(session)
		async for x in (self.filter_updates(updates, session)):
			yield self.format_update(x)

		await session.close()

	async def parse_update_page(self, session=None):
		# inits
		ret= []

		# get all chapters on update page
		main_page= await get_html(self.update_link, session)
		soup= BeautifulSoup(main_page, 'html.parser')

		cards= soup.find_all(class_=["list-item", "rounded"])
		for c in cards:
			up= dict()

			up['series']= c.find(class_='list-title').get_text().strip().replace(' ', '-')
			up['series_link']= c.find(class_='list-title')['href']
			up['chapter_name']= ''
			up['chapter_number']= float(c.find("span", class_="badge-md").get_text().split()[-1])
			up['volume_number']= -1
			up['link']= c.find(class_="media-content")['href']

			ret.append(up)

		return ret

	def parse_series_page(self, soup, update):
		cover_link= soup.find(class_="media-content")['style']
		cover_link= re.search(r":url\((.*)\)", cover_link).groups()[0]
		cover_link= self.home_link + cover_link

		display_name= soup.find(class_="text-highlight").get_text().strip()

		description= soup.select("#content > div > div.row > div.col-lg-9.col-md-8.col-xs-12.text-muted")
		description= description[0].contents[2].strip() # magic

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= self.name,
			group_link= self.home_link,
			site= self.name
		)

	async def get_series_data(self, update, session=None):
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
			s_data= self.parse_series_page(soup, update)
			s_data['link']= link

			# cache
			DATA[name]= s_data
			DATA[name]['last_checked']= time.time()
			utils.dump_json(DATA, utils.SERIES_CACHE)

		return DATA[name]

	async def filter_updates(self, updates, session=None):
		# inits
		ret= []
		SEEN= utils.load_json_with_default(utils.SEEN_CACHE, [])
		BLACKLIST= utils.load_yaml_with_default(utils.BLACKLIST_FILE, default=[])

		for x in updates:
			# inits
			series_data= await self.get_series_data(x, session)
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
			SEEN= SEEN[-12345:]
			utils.dump_json(SEEN, utils.SEEN_CACHE)