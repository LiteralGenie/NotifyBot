import os


ROOT_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"

CONFIG_DIR= ROOT_DIR + "config/"
DATA_DIR= ROOT_DIR + "data/"
CACHE_DIR= ROOT_DIR + "cache/"
WEBVIEW_DIR= ROOT_DIR + "webview/"
LOG_DIR = ROOT_DIR + "logs/"

TEMPLATE_DIR= CONFIG_DIR + "templates/"
SEEN_DIR= CACHE_DIR + "seen/"
SERIES_DIR = CACHE_DIR + "series/"

###

BOT_CONFIG= CONFIG_DIR + "bot_config.yaml"
LOGGING_CONFIG= CONFIG_DIR + "logging.yaml"

ERROR_STRINGS= TEMPLATE_DIR + "errors.yaml"
UPDATE_STRINGS= TEMPLATE_DIR + "updates.yaml"
LOG_STRINGS= TEMPLATE_DIR + "logs.yaml"

MENTIONS_FILE= CONFIG_DIR + "mentions.yaml"
BLACKLIST_FILE= CONFIG_DIR + "series_blacklist.yaml"