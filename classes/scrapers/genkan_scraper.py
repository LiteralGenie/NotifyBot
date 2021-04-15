from utils.scraper_utils import get_html, get_session
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils, time


class GenkanScraper(UpdateScraper):
	def __init__(self, key):
		super().__init__(stop_on_old=True)

		CONFIG= utils.load_bot_config()
		self.home_link= CONFIG[key + '_home_link']
		self.name= CONFIG[key + '_name']
		self.update_link= f"{self.home_link}/latest"

	async def parse_update_page(self, session=None):
		# inits
		ret= []
		page_index= 0


		while True:
			page_index+= 1
			time.sleep(2)

			# get all chapters on update page
			main_page= await get_html(self.update_link + f"?page={page_index}", session)
			soup= BeautifulSoup(main_page, 'html.parser')

			cards= soup.find_all(class_=["list-item", "rounded"])
			if not cards:
				break

			for c in cards:
				up= dict()

				up['series']= c.find(class_='list-title').get_text().strip().replace(' ', '-')
				up['series_link']= c.find(class_='list-title')['href']
				up['chapter_name']= ''
				up['chapter_number']= float(c.find("span", class_="badge-md").get_text().split()[-1])
				up['volume_number']= -1
				up['link']= c.find(class_="media-content")['href']

				yield up

	def parse_series_page(self, soup, update):
		cover_link= soup.find(class_="media-content")['style']
		cover_link= re.search(r":url\((.*)\)", cover_link).groups()[0]
		if "http" not in cover_link:
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