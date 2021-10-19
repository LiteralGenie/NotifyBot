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
        return self.config.home # + f"manga-list.html?listType=pagination&page=1&artist=&author=&group=&m_status=&name=&genre=&ungenre=&sort=last_update&sort_type=DESC"

    def scrape_updates(self) -> list[PartialUpdate]:
        ret = []

        # visit
        resp = self.fetch(self.update_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # scrape
        cards = soup.select('.item-summary')
        for c in cards:
            s_link = c.select_one('.h5 > a')['href']
            if 'https:' not in s_link:
                s_link = self.config.home + s_link

            for ch in c.select('.chapter-item'):
                anchor = ch.select_one('.btn-link')

                # chap num
                chap = anchor.text
                chap = re.match(r"\s*Ch\w*\.?\s*(\d+)(?:\.\d+)?\s*", chap)
                chap = float(chap.group(1))

                # create PartialUpdate
                link = anchor['href']
                if 'https:' not in link:
                    link = self.config.home + link

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
        desc = soup.select_one('.description-summary').text.strip()
        title = soup.select_one('.post-title > h1').text.strip()
        cover = soup.select_one('.summary_image img')['data-src']

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )