import re

from bs4 import BeautifulSoup

from classes import PartialUpdate, SeriesData
from classes.scrapers.update import UpdateScraper


class ArangScraper(UpdateScraper):
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
        cards = soup.select('.card')
        for c in cards:
            # chap num
            chap = c.select_one('.description > p').text
            chap = re.search(r"\d+(?:\.\d+)?", chap)
            chap = float(chap.group(0))

            # series link
            s_link = self.config.home + c.select_one('.header > a')['href']

            # create PartialUpdate
            link = self.config.home + c.select_one('a.button')['href']

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
        desc = soup.select_one('.description > p').text
        title = soup.select_one('.content > h1.header').text

        cover = self.config.home + soup.select_one('.image > img')['src']

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )