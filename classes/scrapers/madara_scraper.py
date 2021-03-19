from utils.scraper_utils import get_html, get_session
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils, time


class MadaraScraper(UpdateScraper):
	def __init__(self, key):
		CONFIG= utils.load_bot_config()
		self.home_link= CONFIG[key + '_home_link']
		self.name= CONFIG[key + '_name']
		self.update_link= f"{self.home_link}"

	async def parse_update_page(self, session=None):
		# inits
		ret= []

		# get all chapters on update page
		main_page= await get_html(self.update_link, session)
		soup= BeautifulSoup(main_page, 'html.parser')

		cards= soup.find_all(class_=["page-item-detail"])
		for c in cards:
			up= dict()

			up['series']= c.find(class_='post-title').get_text().strip()
			up['series_link']= c.find(class_='post-title').find("a")['href']
			up['volume_number']= -1

			for chap in c.find_all(class_="chapter-item"):
				up_copy= up.copy()
				up['chapter_name']= ''
				up['chapter_number']= float(chap.find("a").get_text().strip())
				up['link']= c.find("a")['href']

			ret.append(up)

		return ret

	def parse_series_page(self, soup, update):
		cover_link= soup.find(class_="summary_image").find("img")['src']
		# cover_link= re.search(r":url\((.*)\)", cover_link).groups()[0]
		if "http" not in cover_link:
			cover_link= self.home_link + cover_link

		display_name= soup.find(class_="post-title").find("h1").get_text().strip()
		description= soup.find(class_="summary__content").get_text().strip()

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= self.name,
			group_link= self.home_link,
			site= self.name
		)