from utils.scraper_utils import get_html, get_session
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils, time


class MadaraScraper(UpdateScraper):
	def __init__(self, key):
		super().__init__()
		CONFIG= utils.load_bot_config()
		self.home_link= CONFIG[key + '_home_link']
		self.name= CONFIG[key + '_name']
		self.update_link= f"{self.home_link}"

	async def parse_update_page(self, session=None):
		# inits
		ret= []

		def extract_num(text):
			ch= text                       # Vol. 9 Ch. 74 - New Year's Eve
			ch= ch.split('-')[0].strip()   # Vol. 9 Ch. 74
			ch= re.sub(".*?ch[^\d]*", "", ch, flags=re.IGNORECASE)
			return float(ch)

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
				up_copy['chapter_name']= ''
				up_copy['chapter_number']= float(extract_num(chap.find("a").get_text()))
				up_copy['link']= chap.find("a")['href']
				yield up_copy

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