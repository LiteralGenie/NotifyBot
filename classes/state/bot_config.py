from typing import TypedDict, List

from classes.state.proxy_dict import ProxyDict
from utils import load_yaml_with_default, BOT_CONFIG


# mostly for typing / intellisense
class BotConfig:
    def __init__(self):
        self._cfg = self.load()

        self.key: str = self['discord_key']
        self.prefix: str = self['prefix']
        self.error_channel: int = self['error_channel']
        self.global_pings: list[int] = self['global_pings']

        self.msg_delay: int = self['msg_delay']
        self.error_delay: int = self['error_delay']

        self.defaults: IDefaults = self['defaults']

    def load(self):
        self._cfg = load_yaml_with_default(BOT_CONFIG, default=False)
        return self._cfg

    def __getitem__(self, key):
        val = self._cfg[key]
        if isinstance(val, dict):
            return ProxyDict(self, key)
        else:
            return val

    def _get(self, key):
        return self._cfg[key]


# interface for scraper defaults (dict)
class IDefaults(TypedDict):
    freq: int
    s_refresh: int
    block_type: int
    pings: List[int]
