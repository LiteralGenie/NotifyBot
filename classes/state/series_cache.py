from dataclasses import asdict

import utils
from classes import SeriesData


class SeriesCache:
    def __init__(self, site_name):
        self.fp = utils.SERIES_DIR + f"{site_name}.json"
        self.cache = self.load()

    def load(self):
        self.cache = utils.load_json_with_default(self.fp, {})
        return self.cache

    def dump(self):
        utils.dump_json(self.cache, self.fp)

    def add(self, key: str, data: SeriesData):
        self.cache[key.lower()] = asdict(data)
        self.dump()

    def get(self, key: str, scrape_fn, *args, **kwargs):
        key = key.lower()

        if key not in self.cache:
            data = scrape_fn(*args, **kwargs)
            self.add(key, data)

        return SeriesData(**self.cache[key])