from utils.scraper_utils import get_html
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils


class MdScraper(UpdateScraper):
	@classmethod
	async def parse_update_page(cls, session=None):
		# inits
		ret= []
		CONFIG= utils.load_bot_config()

		# get all chapters on update page
		main_page= await get_html(CONFIG['mangadex_update_link'], session)
		soup= BeautifulSoup(main_page, 'lxml')

		items= soup.find_all("item")
		for it in items:
			up= dict()

			# Asuperu Kanojo - Volume 5, Chapter 38
			tmp= it.find('title').get_text().split()

			# series
			up['series']= [tmp.pop(0)]
			while not (tmp[0] == "-" and ("Chapter" in tmp[1] or "Volume" in tmp[1])):
				up['series'].append(tmp.pop(0))

			up['series']= "-".join(up['series'])
			tmp.pop(0) # -

			# volume / chapter
			up['volume_number']= -1

			typ= tmp.pop(0)
			num= tmp.pop(0)
			if typ == "Volume":
				up['volume_number']= int(num.replace(",",""))
				typ= tmp.pop(0)
				num= tmp.pop(0)

			assert typ == 'Chapter'
			up['chapter_number']= float(num)

			# chap name
			up['chapter_name']= ''

			# chap link
			up['link']= it.find('guid').get_text()

			# series_link
			up['series_link']= it.find('mangalink').get_text()

			# group
			tmp= it.find("description").get_text().split() # Group: Spruce Tree Scanlations - Uploader: Seele - Language: English

			while tmp[0] != "Group:":
				tmp.pop(0)
			tmp.pop(0)

			group= [tmp.pop(0)]
			while tmp[0] != "-" and tmp[1] != "Uploader:":
				group.append(tmp.pop(0))
			up.setdefault('extra', {})['group']= " ".join(group)

			ret.append(up)

		return ret


	@staticmethod
	def parse_series_page(soup, update):
		cover_link= soup.find(title="See covers").find("img")['src']
		display_name= soup.find(class_=["card", "mb-3"]).find(class_="mx-1").get_text().strip()
		description= ""

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= update['extra']['group'],
			group_link="https://mangadex.org/",
			site= "mangadex"
		)