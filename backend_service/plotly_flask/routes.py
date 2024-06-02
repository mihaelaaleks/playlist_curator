"""Routes for parent Flask app."""

from flask import render_template, flash, redirect, url_for, request
from flask import current_app as app


from plotly_flask.models import curator_logic, playlist_logic
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
    spotify = curator_logic.create_spotify()
    form = CuratorForm(request.form)
    if request.method == "GET":
        genres = curator_logic.get_genre_seeds(spotify)
        form.genre_select.choices = genres
    playlist_list = playlist_logic.df_to_playlist_obj()
    track_recommendations = []
    if request.method == "POST":
        form_result = request.form.to_dict(flat=False)
        print(form_result["artist_select"])
        print(form_result["track_select"])
        genre_select_result = form_result["genre_select"]
        print(curator_logic.split_into_chunks(genre_select_result))
        recommended_tracks = curator_logic.get_multi_recommendation_tracks(spotify, genre_select_result)
        return render_template(
            "recommended_panel.html", track_recommendations=recommended_tracks
        )
    return render_template(
        "curator.html",
        playlists=playlist_list,
        track_recommendations=track_recommendations,
        form=form,
        template="curator-template",
    )
    

