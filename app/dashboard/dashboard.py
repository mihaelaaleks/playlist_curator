import pandas as pd
import dash
import pathlib
import plotly.express as px

data_path = pathlib.Path(__file__).parent.parent / pathlib.Path('data')

df = pd.read_pickle(data_path / pathlib.Path('audio_analysis_df.pkl'))


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel" : "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def header_layout():
    dash.html.Div(
            children=[
                dash.html.P(children="🎵", className="header-emoji"),
                dash.html.H1(
                    children="In-depth Spotify Analytics", className="header-title"
                ),
                dash.html.P(
                    children=(
                        "Analyze your listening behaviour"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        )

# app layout
app.layout = dash.html.Div([
    dash.html.Div(children='Spotify Analysis Tool'),
    dash.html.Hr(),
    dash.dcc.RadioItems(options=['energy', 'valence', 'danceability'], value='energy', id='controls-and-radio-item'), 
    dash.dash_table.DataTable(data = df.to_dict('records'), page_size=6),
    dash.dcc.Graph(figure={}, id='controls-and-graph')
])

# add controls to build the interaction
@dash.callback(
    # need ids for this to work
    dash.Output(component_id='controls-and-graph', component_property='figure'),
    dash.Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='artist_name', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)