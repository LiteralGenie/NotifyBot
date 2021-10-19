import re

from bs4 import BeautifulSoup

from classes import PartialUpdate, SeriesData
from classes.scrapers.update import UpdateScraper
from utils.scraper_utils import extract_num


class MadaraScraper(UpdateScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_link = self.config.home
        self.group_name = self.config.name

    @property
    def update_link(self):
        return self.config.home + f"m/manga/?m_orderby=latest"

    def scrape_updates(self) -> list[PartialUpdate]:
        ret = []

        # visit
        resp = self.fetch(self.update_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # scrape
        cards = soup.select('.page-item-detail.manga')
        for c in cards:
            # get chap nums
            chaps = c.select('.chapter')
            chaps.sort(reverse=True, key=extract_num)

            # series link
            s_link = c.select_one('.item-thumb > a')['href']

            # ignore externally hosted chaps
            if "bilibili" in c.text.lower():
                # todo: logging
                continue

            # create PartialUpdate
            for ch in chaps:
                link = ch.select_one('a')['href']
                chap = extract_num(ch)

                ret.append(PartialUpdate(
                    link=link,
                    chap=chap,
                    group_name=self.group_name,
                    group_link=self.group_link,
                    series_link=s_link,
                ))

        return ret

    # scrape series data
    def scrape_data(self, up: PartialUpdate) -> SeriesData:
        # visit
        resp = self.fetch(up.series_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # extract info
        try: desc = soup.select_one('.summary__content').text
        except: desc = ""

        title = soup.select_one('.post-title > h1').text

        script = soup.select_one("""script[type="application/ld+json"]""")
        cover = re.search(r'url": "(.*)",', str(script)).group(1)

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )