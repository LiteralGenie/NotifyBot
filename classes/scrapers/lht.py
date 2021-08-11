import re

from bs4 import BeautifulSoup

from classes import PartialUpdate, SeriesData
from classes.scrapers.update import UpdateScraper


class LhtScraper(UpdateScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_link = self.config.home
        self.group_name = self.config.name

    @property
    def update_link(self):
        return self.config.home + f"manga-list.html?listType=pagination&page=1&artist=&author=&group=&m_status=&name=&genre=&ungenre=&sort=last_update&sort_type=DESC"

    def scrape_updates(self) -> list[PartialUpdate]:
        ret = []

        # visit
        resp = self.session.get(self.update_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # scrape
        cards = soup.select('.media')
        for c in cards:
            # chap num
            chap = c.select('a')[-1]
            chap = float(chap.text)

            # series link
            s_link = self.config.home + c.select_one('.media-heading > a')['href']

            # create PartialUpdate
            link = self.config.home + c.select('a')[-1]['href']

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
        resp = self.session.get(up.series_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # extract info
        desc = soup.select('.well > .row:nth-child(3) > p')
        desc = "\n".join([x.text for x in desc])
        title = soup.select_one('.manga-info > h1').text

        cover = soup.select_one('.thumbnail')['src']

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )