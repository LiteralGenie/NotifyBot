from typing import List

from classes import Update
from classes.state.bot_config import IDefaults
from classes.state.proxy_dict import ProxyDict
from utils import contains_all


class ScraperConfig:
    name: str
    home: str
    out: int
    filter_list: list[str]

    # optionals -- same as IDefaults
    freq: int
    s_refresh: int
    filter_type: int
    pings: List[int]

    def __init__(self, defaults: IDefaults, cfg: ProxyDict):
        self._defaults = defaults
        self._cfg = cfg

    def __getattr__(self, item):
        return self._cfg.get(item) or self._defaults[item] # type: ignore

    def is_blocked(self, update: Update) -> bool:
        hash = update.title
        match_result = True if (self.filter_type == 0) else False # blacklist if block_type == 0, whitelist otherwise

        for string in self.filter_list:
            if contains_all(hash, string):
                return match_result
        else:
            return not match_result

    @property
    def update_link(self) -> str:
        raise NotImplementedError