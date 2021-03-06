from utils.scraper_utils import get_html
from classes.scrapers import UpdateScraper
from bs4 import BeautifulSoup
import re, utils


class SushiScraper(UpdateScraper):
	def __init__(self):
		super().__init__()

	async def parse_update_page(self, session=None):
		updates= [self.parse_chap_url(x) for x in await self.get_update_urls(session)]
		for x in updates:
			yield x

	def parse_series_page(self, soup, update):
		cover_link= soup.find(class_="summary_image").find('img')['data-src']
		display_name= soup.find(class_="post-title").get_text().strip()
		description= soup.find(class_="summary__content").get_text().strip()

		return dict(
			cover_link=cover_link,
			display_name=display_name,
			description=description,
			group= "Mangasushi",
			group_link="https://mangasushi.net",
			site= "mangasushi"
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
			volume_number=-1,
			link=url
		)


	@staticmethod
	async def get_update_urls(session=None):
		# inits
		ret= []
		CONFIG= utils.load_bot_config()

		# get all chapters on update page
		main_page= await get_html(CONFIG['sushi_update_link'], session)
		soup= BeautifulSoup(main_page, 'html.parser')

		series_group= soup.find_all(class_="page-item-detail manga")
		for x in series_group:
			ret+= [y['href'] for y in x.find(class_="list-chapter").find_all("a")]

		# return
		return ret