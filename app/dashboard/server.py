import dash
from dash import html
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple # this is only suitable for development
# gunicorn should be used to actually serve the app when its ready
from dashboard import app

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"

@server.route("/dash")
def dash_app():
    return app.index()

app1 = dash.Dash(requests_pathname_prefix="/app1/")
app1.layout = app.layout


application = DispatcherMiddleware(
    server, 
    {"/app1": app1.server}
)

if __name__ == "__main__":
    run_simple("localhost", 8050, application)