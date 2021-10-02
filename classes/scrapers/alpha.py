import re
import time

from bs4 import BeautifulSoup

from classes import PartialUpdate, SeriesData
from classes.scrapers.update import UpdateScraper


class AlphaScraper(UpdateScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_link = self.config.home
        self.group_name = self.config.name

    @property
    def update_link(self):
        return self.config.home

    def scrape_updates(self) -> list[PartialUpdate]:
        ret = []

        # visit
        resp = self.fetch(self.update_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # scrape
        cards = soup.select('.listupd')
        cards = cards[2].select('.bsx > a')

        for c in cards:
            # chap num
            chap = c.select_one('.epxs').text
            chap = re.search(r"Chapter (\d+(?:\.\d+)?)", chap)
            if chap:
                chap = float(chap.group(1))
            else:
                chap = int(time.time())

            # create PartialUpdate
            link = c['href']

            # series link
            s_link = re.sub(r'-chapter-\d+/?', '', link, flags=re.IGNORECASE)

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
        desc = soup.select_one('.info-desc .entry-content').text
        title = soup.select_one('.entry-title').text

        cover = soup.select_one('.thumb > .wp-post-image')['src']

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )