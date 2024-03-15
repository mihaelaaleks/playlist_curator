import dash
import dash_bootstrap_components as dbc
from assets import style

def header():
    header = dash.html.Div(
            children=[
                dash.html.H1(
                    children="In-depth Spotify Analytics （＾Ｏ＾☆♪", className="header-title"
                ),
            ],
            className="header",
        )
    return header

def sidebar(user_display_name, playlist_names_navlinks):
    sidebar = dash.html.Div(
         [
        dash.html.H2("Welcome back", className="display-5"),
        dash.html.H2(f"{user_display_name}", className="display-6"),
        dash.html.Hr(),
        dash.html.P(
            "Your current playlists", className="lead"
        ),
        dash.html.Hr(),
        dbc.Nav(
            children = playlist_names_navlinks,
            vertical=True,
            pills=True,
            className = "navbar",
        ),
        
    ],
    className="vh-100",
    style=style.SIDEBAR_STYLE,
    )
    
    return sidebar

def main_body(): 
    body = dash.html.Div(id='main-content',children = [],  style=style.CONTENT_STYLE)
    return body

## TO-DO MAKE CARD TO DISPLAY PLAYLIST IMAGE, NAME AND DESCRIPTION AS A START
def playlist_card(): 
    ...