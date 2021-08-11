import utils
from classes import AmyBotU

utils.configure_logging()


bot= AmyBotU(case_insensitive=True)
bot.start_bot()