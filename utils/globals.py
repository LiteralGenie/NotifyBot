import os


ROOT_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"

CONFIG_DIR= ROOT_DIR + "config/"
DATA_DIR= ROOT_DIR + "data/"
CACHE_DIR= ROOT_DIR + "cache/"
TEMPLATE_DIR= ROOT_DIR + "templates/"


###

BOT_CONFIG= CONFIG_DIR + "bot_config.yaml"
LOGGING_CONFIG= CONFIG_DIR + "logging_config.yaml"

ERROR_STRINGS= TEMPLATE_DIR + "errors.yaml"
UPDATE_STRINGS= TEMPLATE_DIR + "updates.yaml"
LOG_STRINGS= TEMPLATE_DIR + "logs.yaml"

SERIES_CACHE= CACHE_DIR + "series.json"
SEEN_CACHE= CACHE_DIR + "seen.json"

MENTIONS_FILE= CONFIG_DIR + "mentions.yaml"