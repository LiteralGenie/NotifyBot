import asyncio, logging
from typing import Generator, Iterable
from requests import Session

from classes import Update, PartialUpdate, SeriesData
from classes.state.scraper_config import ScraperConfig
from classes.state.seen_cache import SeenCache
from classes.state.series_cache import SeriesCache

LOG = logging.getLogger('debug')


class UpdateScraper:
    # scrape update page
    def scrape_updates(self) -> list[PartialUpdate]:
        raise NotImplementedError

    # scrape series data
    def scrape_data(self, up: PartialUpdate) -> SeriesData:
        raise NotImplementedError



    def __init__(self, config: ScraperConfig, session: Session):
        self.config = config
        self.seen = SeenCache(config.name)
        self.series = SeriesCache(config.name)
        self.session = session

    async def loop(self) -> Generator[Update, None, None]:
        while True:
            async for up in self.get_updates():
                yield up

            await asyncio.sleep(self.config.freq)


    async def get_updates(self) -> Generator[Update, None, None]:
        # parse update page
        LOG.info(f'[{self.config.name}] Scanning updates')
        partial_updates = self.scrape_updates()

        LOG.info(f'[{self.config.name}] Loading data {len(partial_updates)}')
        updates = [self.load_data(up) for up in partial_updates]

        # filter
        LOG.info(f'[{self.config.name}] Filtering updates {len(updates)}')
        ftrd = self.filter_updates(updates)

        # return
        for up in ftrd:
            LOG.info(f'[{self.config.name}] Yielding update {up.link}')
            yield up
            self.seen.add(up.hash)

    # get and cache series data
    def load_data(self, up: PartialUpdate) -> Update:
        data = self.series.get(
            up.series_link,
            self.scrape_data, up
        )

        return Update(up, data)

    def filter_updates(self, updates: Iterable[Update]) -> Generator[Update, None, None]:
        for up in updates:
            # check seen
            if up.hash in self.seen:
                continue

            # check blocklist
            if self.config.is_blocked(up):
                continue

            # return
            yield up

    def fetch(self, link, timeout=15, **kwargs):
        return self.session.get(link, timeout=timeout, **kwargs)