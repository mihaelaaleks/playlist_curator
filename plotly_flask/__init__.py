"""Initialize Flask App"""
from flask import Flask

"""Construct core Flask application"""
def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():
        # import parts of the core Flask app
        from . import routes
        
        # import dash application
        from .plotly_dash.dashboard import create_dashboard
        app = create_dashboard(app)
        
        return app