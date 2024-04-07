from dash import Dash, html, dcc, Input, Output
from plotly_flask.models import playlist_logic
import plotly.express as px

PLAYLIST_ID = "7doP9xG2n6DXnflGTmURsC"


def create_dashboard(server):
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "../static/basic_ui.css",
        ],
    )

    # load dataframe
    # df = playlist_logic.get_tracklist_w_labels(PLAYLIST_ID)
    # artist_counts = df['artist_name'].value_counts()
    # fig = px.pie(names=artist_counts.index, values=artist_counts.values, title='Artist Counts')
    # fig.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+percent')
    # create dash layout
    dash_app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=True),
            dcc.Graph(
                id="pie-chart",
            ),
        ]
    )

    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output("pie-chart", "figure"), [Input("url", "pathname")])
    def update_pie_chart(pathname):
        # When pathname is like:
        #   "/dashapp/0e8tuDsddlctM6tBDEYPJ2/"
        # running
        #   "/dashapp/0e8tuDsddlctM6tBDEYPJ2/".split("/")
        #   => ['', 'dashapp', '0e8tuDsddlctM6tBDEYPJ2', '']
        # The -2 is two spaces back from the end to get the id
        PATH_SPLIT_INDEX = -2

        print(f"Pathname:{pathname}")
        playlist_id = pathname.split("/")[PATH_SPLIT_INDEX]
        print(f"playlist id:{playlist_id}")

        df = playlist_logic.get_tracklist_w_labels(playlist_id)
        artist_counts = df["artist_name"].value_counts()

        # Create pie chart
        fig = px.pie(
            names=artist_counts.index,
            values=artist_counts.values,
            title="Artist Counts",
        )
        fig.update_traces(
            textposition="inside", textinfo="percent+label", hoverinfo="label+percent"
        )

        return fig
