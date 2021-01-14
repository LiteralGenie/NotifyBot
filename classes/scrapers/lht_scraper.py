from utils.scraper_utils import get_html
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import utils


class LhtScraper(UpdateScraper):
	@classmethod
	async def parse_update_page(cls, session=None):
		# inits
		ret= []
		CONFIG= utils.load_bot_config()

		# get all chapters on update page
		main_page= await get_html(CONFIG['lht_update_link'], session)
		soup= BeautifulSoup(main_page, 'html.parser')

		cards= soup.find_all(class_=["itemupdate"])
		for c in cards:
			up= dict()

			up['series']= c.find(class_='title-h3').get_text().strip().replace(' ', '-')
			up['series_link']= r"https://lhtranslation.net/" + c.find(class_='title-h3-link')['href']
			up['chapter_name']= ''
			up['volume_number']= -1
			up['link']= r"https://lhtranslation.net/" + c.find(class_="chapter")['href']

			tmp= c.find(class_="chapter").get_text().split("-")[-1]
			tmp= float(tmp.split()[-1])
			up['chapter_number']= tmp

			ret.append(up)

		return ret

	@staticmethod
	def parse_series_page(soup, update):
		cover_link= soup.find(class_="thumbnail")['src']

		display_name= soup.find(class_="manga-info").find('h1').get_text().strip().title()

		description= soup.find(class_="well well-sm")
		description= description.find_all(class_="row")
		description= description[1].find_all("p")
		description= "\n".join(x.get_text().strip() for x in description)

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= "LHT",
			group_link="https://lhtranslation.net/",
			site= "lhtranslation"
		)