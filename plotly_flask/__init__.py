"""Initialize Flask App"""
from flask import Flask

# session = Session()


def init_app():
    """Construct core Flask application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    # Initialize Plugins
    # e.g. session.init_app(app)
    
    with app.app_context():
        # import parts of the core Flask app
        from . import routes

        # import dash application
        from .plotly_dash.dashboard import create_dashboard
        app = create_dashboard(app)
        
        return app