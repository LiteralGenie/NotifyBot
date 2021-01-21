import utils
from bot import AmyBotU

# inits
CONFIG= utils.load_bot_config()
bot= AmyBotU(case_insensitive=True)

# run
bot.run(CONFIG['discord_key'])