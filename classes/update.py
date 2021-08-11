import re

from dataclasses import dataclass


def cln_link(link):
    return re.sub("(?<!:)/+", "/", link)

@dataclass
class PartialUpdate:
    link: str
    chap: float

    group_name: str
    group_link: str
    series_link: str

    vol: float = -1

    def __post_init__(self):
        self.series_link = cln_link(self.series_link)
        self.group_link = cln_link(self.group_link)
        self.link = cln_link(self.link)


@dataclass
class SeriesData:
    title: str
    desc: str

    cover_link: str = ""

    def __post_init__(self):
        self.desc = self.desc.strip()
        self.title= self.title.strip()
        self.cover_link = cln_link(self.cover_link)


class Update(PartialUpdate, SeriesData):
    def __init__(self, update: PartialUpdate, series_data: SeriesData):
        self.__dict__ = {**update.__dict__, **series_data.__dict__}

    @property
    def hash(self):
        return f"{self.title} || {self.chap} || {self.vol}"

