import utils


class SeenCache:
    def __init__(self, site_name):
        self.fp = utils.SEEN_DIR + f"{site_name}.json"
        self.cache = self.load()

    def load(self):
        self.cache = set(utils.load_json_with_default(self.fp, []))
        return self.cache

    def dump(self):
        utils.dump_json(list(self.cache), self.fp)

    def add(self, hash):
        self.cache.add(hash)
        self.dump()

    def __contains__(self, item):
        return item in self.cache