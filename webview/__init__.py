from discord.ext import ipc
from . import web_utils
import os, utils


# paths
BASE_DIR= os.path.dirname(__file__)

# connect to discord bot
_config= utils.load_bot_config()
IPC_CLIENT = ipc.Client(
    secret_key=_config['ipc_key'],
    port=_config['ipc_port']
)