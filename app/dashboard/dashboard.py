import pandas as pd
import dash
from pathlib import Path
import dash_bootstrap_components as dbc
from assets import style
from templates import playlist_templates as pt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, style.FONT_AWESOME, 'assets/style.css'])

data_path = Path(__file__).parent.parent / Path('data')

playlist_df = pd.read_pickle(data_path / Path('my_cleaned_playlist.pkl'))

# create a dictionary from the playlist ids and names
playlist_items = dict(zip(playlist_df.id, playlist_df.name))
user_display_name = playlist_df['owner'][0]['display_name']

def playlist_names_navlinks():
    list_of_buttons = []
    for id, name in playlist_items.items(): 
        list_of_buttons.append(dbc.NavLink(f"{name}", 
                                           active="exact", 
                                           id={
                                               "type": "playlist_name_display",
                                               "index": id},
                                           href = f'/{id}',
                                           external_link=True))
    return list_of_buttons
        
content = dash.html.Div(id='page-content',children = [pt.header(), pt.main_body()],  style=style.CONTENT_STYLE)

app.layout = dash.html.Div([dash.dcc.Location(id="url"), pt.sidebar(user_display_name, playlist_names_navlinks()), content])

@app.callback(
    # in this case no match would be needed 
    # since the component would be generated from the callback
    dash.Output('main-content', 'children'),
    dash.Input("url", "pathname"),
    # pass along the id of the navlink into the callback
        # i need to figure how state works in dash, 
        # the below throws errors 
    # dash.State("session-store", "data")
)
def show_playlist_info(pathname):
    id_from_pathname = pathname.split('/')[-1]
    playlist = playlist_items.get(id_from_pathname)
    return playlist

if __name__ == '__main__':
    app.run(debug=True)