from quart import Quart, Response
from . import root, settings


app= Quart(__name__)
app.register_blueprint(root.bp)
app.register_blueprint(settings.bp)

if __name__ == "__main__":
	app.run(debug=True)