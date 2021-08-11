import re

from bs4 import BeautifulSoup

from classes import PartialUpdate, SeriesData
from classes.scrapers.update import UpdateScraper


class GenkanScraper(UpdateScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_link = self.config.home
        self.group_name = self.config.name

    @property
    def update_link(self):
        return self.config.home + f"latest"

    def scrape_updates(self) -> list[PartialUpdate]:
        ret = []

        # visit
        resp = self.session.get(self.update_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # scrape
        cards = soup.select('.list-item')
        for c in cards:
            # chap num
            num = c.select_one('.text-uppercase').text

            _fl = r"\d+(?:\.\d+)?"
            m = re.search(rf"Vol\. ({_fl}) Ch\. ({_fl})", num)
            vol = float(m.group(1))
            chap = float(m.group(2))

            # series link
            s_link = c.select_one('.list-title')['href']

            # create PartialUpdate
            link = c.select_one('.media-content')['href']

            ret.append(PartialUpdate(
                link=link,
                chap=chap,
                vol=vol,
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
        desc = soup.select_one('.col-lg-9')
        desc = [x for x in desc.children if x != "\n"]
        desc = desc[1]
        title = soup.select_one('h5.text-highlight').text

        cover = soup.select_one('.media-content')['style']
        cover = re.search(r'background-image:url\((.*)\)', cover)
        cover = self.config.home + cover.group(1)

        # return
        return SeriesData(
            title=title,
            desc=desc,
			cover_link=cover,
        )