"""Flask App configuration."""
from os import environ, path
from dotenv import load_dotenv
import redis

# Specify a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask config variables."""

    # General Config
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    # Spotipy
    SPOTIPY_CLIENT_ID = environ.get("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = environ.get("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = environ.get("SPOTIPY_REDIRECT_URI")
    
    # Flask-Session
    # REDIS_URI = environ.get("REDIS_URI")
    # SESSION_TYPE = "redis"
    # SESSION_REDIS = redis.from_url(REDIS_URI)
