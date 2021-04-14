from webview.app import app
import utils


config= utils.load_bot_config()
app.run(host="0.0.0.0", port=config['http_port'])