from utils.scraper_utils import get_html
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils


class LeviScraper(UpdateScraper):
	@classmethod
	async def parse_update_page(cls, session=None):
		# inits
		ret= []
		CONFIG= utils.load_bot_config()

		# get all chapters on update page
		main_page= await get_html(CONFIG['leviathan_update_link'], session)
		soup= BeautifulSoup(main_page, 'html.parser')

		cards= soup.find_all(class_="list-item rounded")
		for c in cards:
			up= dict()

			up['series']= c.find(class_='list-title').get_text().replace(' ', '-')
			up['series_link']= c.find(class_='list-title')['href']
			up['chapter_name']= ''
			up['chapter_number']= float(c.find("span", class_="badge-md").get_text().split()[-1])
			up['link']= c.find(class_="media-content")['href']

			ret.append(up)

		return ret

	@staticmethod
	def parse_series_page(soup):
		cover_link= soup.find(class_="media-content")['style']
		cover_link= re.search(r":url\((.*)\)", cover_link).groups()[0]
		cover_link= "https://leviatanscans.com/" + cover_link

		display_name= soup.find(class_="text-highlight").get_text().strip()

		description= soup.select("#content > div > div.row > div.col-lg-9.col-md-8.col-xs-12.text-muted")
		description= description[0].contents[2].strip() # magic

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= "Leviatan Scans",
			group_link="https://leviatanscans.com/",
		)

	@staticmethod
	def parse_chap_url(url):
		# inits
		CONFIG= utils.load_bot_config()
		def clean(x):
			return x.replace("-","_").strip()

		# parse url
		m= re.search(r".*mangasushi.net/manga/(.*)/chapter-(\d+)(?:-(\d+))?(?:-(.*))?/", url).groups()

		# clean results
		series= clean(m[0])

		chapter_num= m[1]
		if m[2] is not None:
			chapter_num+= f".{m[2]}"
		chapter_num= float(chapter_num)

		chapter_name= ""
		if m[3]:
			chapter_name= chapter_name

		# return
		return dict(
			series=series,
			series_link= CONFIG['sushi_series_base'] + m[0],
			chapter_name=chapter_name,
			chapter_number=chapter_num,
			link=url
		)