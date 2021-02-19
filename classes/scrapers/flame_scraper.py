from utils.scraper_utils import get_html, get_session
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils, time


class FlameScraper(UpdateScraper):
	def __init__(self):
		CONFIG= utils.load_bot_config()
		self.series_base= CONFIG['flame_series_base']
		self.update_link= CONFIG['flame_update_link']
		self.config= CONFIG

	async def parse_update_page(self, session=None):
		# inits
		ret= []

		# get all chapters on update page
		main_page= await get_html(self.update_link, session)
		soup= BeautifulSoup(main_page, 'html.parser')

		cards= soup.find_all(class_=["uta"])
		for c in cards:
			up= dict()

			up['series']= c.find(class_='series')['title']
			up['series_link']= c.find(class_='series')['href']
			up['chapter_name']= ''
			up['volume_number']= -1

			for x in c.find('ul').find_all('a'):
				chap= up.copy()
				chap['link']= x['href']
				chap['chapter_number']= float(re.search(r'Chapter (\d+(?:\.\d+)?)', x.get_text()).groups()[0])
				ret.append(chap)

		return ret

	def parse_series_page(self, soup, update):
		cover_link= soup.find(class_="wp-post-image")['src']
		# cover_link= re.search(r":url\((.*)\)", cover_link).groups()[0]
		# if "http" not in cover_link:
		# 	cover_link= self.home_link + cover_link
		assert 'http' in cover_link

		display_name= soup.find(class_="entry-title").get_text().strip()
		description= soup.find(class_='entry-content').get_text().strip()

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= 'Flame Scans',
			group_link= 'https://flamescans.org/',
			site= 'flamescans'
		)