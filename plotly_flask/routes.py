"""Routes for parent Flask app."""

from flask import render_template, flash, redirect, url_for, request
from flask import current_app as app


from plotly_flask.models import playlist_logic
from plotly_flask.models import curator_logic
from .forms import CuratorForm


@app.route("/")
def home():
    """Landing page."""
    playlist_list = playlist_logic.df_to_playlist_obj()
    return render_template(
        "index.html",
        title="Plotly Dash Flask Tutorial",
        description="Embed Plotly Dash into your Flask applications.",
        template="index",
        playlists=playlist_list,
        body="This homepage is served with Flask.",
    )


@app.route("/dashboard", methods=["GET", "POST"])
def show_playlist_dashboard():
    """Playlist statistics page."""
    playlist_list = playlist_logic.df_to_playlist_obj()
    return render_template(
        "dashboard.html", playlists=playlist_list, template="info-template"
    )


@app.route("/dashboard/<playlist_id>", methods=["GET", "POST"])
def show_playlist(playlist_id):
    tracklist = playlist_logic.get_tracklist(playlist_id=playlist_id)
    playlist_list = playlist_logic.df_to_playlist_obj()
    avg_popularity = playlist_logic.get_avg_popularity(tracklist)
    return render_template(
        "dashboard.html",
        tracklist=tracklist,
        playlist_id = playlist_id,
        playlists=playlist_list,
        avg = avg_popularity,
    )


@app.route("/curator", methods=["GET", "POST"])
def curator():
    """Playlist curator page."""
    playlist_list = playlist_logic.df_to_playlist_obj()
    form = CuratorForm(request.form)
    track_recommendations = []
    if request.method == "POST":

        spotify = curator_logic.create_spotify()
        track_recommendations = curator_logic.get_cleaned_recommendations(
            limit=50,
            spotify=spotify,
            t_acousticness=form.acousticness.data,
            t_danceability=form.danceability.data,
            t_energy=form.energy.data,
            t_instrumentalness=form.instrumentalness.data,
        )
        return render_template(
            "recommended_panel.html", track_recommendations=track_recommendations
        )
    return render_template(
        "curator.html",
        playlists=playlist_list,
        track_recommendations=track_recommendations,
        form=form,
        template="curator-template",
    )
