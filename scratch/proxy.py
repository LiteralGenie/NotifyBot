# so that when config is updated, objects using it will also get updated
class ProxyDict:
    def __init__(self, parent, key):
        self._parent = parent
        self._key = key

    def __getitem__(self, key):
        val = self._get(key)
        # val = self._parent[self._key][key]
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

class Config:
    def __init__(self):
        self._cfg = dict(d1=dict(d2=dict(v='3')))

    def __getitem__(self, key):
        val = self._cfg[key]
        if isinstance(val, dict):
            return ProxyDict(self, key)
        else:
            return val

    def _get(self, key):
        return self._cfg[key]

c = Config()

dct = c['d1']['d2']
print(dct['v'])

c._cfg = dict(d1=dict(d2=dict(v='5')))
print(dct['v'])

print(dct.get('b'))