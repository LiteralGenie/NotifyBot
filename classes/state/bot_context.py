import requests


# holds app state
from classes.state.bot_config import BotConfig


class BotContext:
    def __init__(self):
        self.session = self.load_session()
        self.config = BotConfig()

    def load_session(self):
        self.session = requests.Session()
        return self.session