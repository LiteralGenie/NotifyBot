# so that when config is updated, objects using it will also get updated
class ProxyDict:
    def __init__(self, parent, key):
        self._parent = parent
        self._key = key

    def __getitem__(self, key):
        val = self._get(key)
        if isinstance(val, dict):
            return ProxyDict(self, key)
        else:
            return val

    def _get(self, key):
        return self._parent._get(self._key)[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default