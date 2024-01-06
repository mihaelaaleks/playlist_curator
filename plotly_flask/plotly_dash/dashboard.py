from dash import Dash, html

def create_dashboard(server):
    dash_app = Dash(
        server = server, 
        routes_pathname_prefix = '/dashapp/',
        external_stylesheets=['../static/style.css',
                              '../static/style.py']
    )
    
    # create dash layout
    dash_app.layout = html.Div(id='dash-container')
    
    return dash_app.server