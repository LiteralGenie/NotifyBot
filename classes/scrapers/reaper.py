from classes.scrapers import MadaraScraper


class ReaperScraper(MadaraScraper):
    @property
    def update_link(self):
        return self.config.home + "home1/"