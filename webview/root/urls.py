from quart import Blueprint
from . import views


bp= Blueprint("root", __name__)
bp.add_url_rule("/", view_func=views.home)



# for ease of development -- will be aggregated for production server
def static(static_type, mimetype=None):
	import utils, glob, os
	from quart import send_file

	async def func(file_path):
		for x in glob.glob(utils.WEBVIEW_DIR + f"*/{static_type}/*.{static_type}"):
			if os.path.basename(x).lower() == os.path.basename(file_path).lower():
				return await send_file(x, mimetype=mimetype)
		return ""
	return func
bp.add_url_rule("/js/<path:file_path>/", endpoint="js", view_func=static('js', mimetype="application/javascript"))
bp.add_url_rule("/css/<path:file_path>/", endpoint="css", view_func=static('css'))