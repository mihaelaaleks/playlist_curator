"""Routes for parent Flask app."""

from flask import Request
from flask import current_app as app
from flask import jsonify, redirect, render_template, request
from spotipy import Spotify

from plotly_flask.models import curator_logic, playlist_logic

from .forms import CuratorForm, CuratorTypeForm


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
        playlist_id=playlist_id,
        playlists=playlist_list,
        avg=avg_popularity,
    )


def _do_curator_from_scratch_post(spotify: Spotify, form: CuratorForm) -> str:
    genre_select_result = form.genre_select.data
    recommended_tracks = curator_logic.get_multi_recommendation_tracks(
        spotify, genre_select_result
    )
    return render_template(
        "recommended_panel.html", track_recommendations=recommended_tracks
    )


@app.route("/curator/", methods=["GET", "POST"])
def curator():
    """Playlist curator page."""
    form: CuratorTypeForm = CuratorTypeForm()
    if form.validate_on_submit():
        if form.from_scratch.data:
            return redirect("from_scratch")
        elif form.from_playlist.data:
            return redirect("from_playlist")
    return render_template("curator.html", form=form)


@app.route("/api/playlists", methods=["GET"])
def get_playlists():
    playlists = playlist_logic.df_to_playlist_obj()
    playlist_data = [
        {"id": playlist.id, "name": playlist.name, "image": playlist.image}
        for playlist in playlists
    ]
    return jsonify(playlist_data)


@app.route("/curator/<curator_type>", methods=["GET", "POST"])
def curator_redirect(curator_type):
    if curator_type == "from_scratch":
        return _curator_from_scratch(request)
    elif curator_type == "from_playlist":
        return _curator_from_playlist(request)


def _curator_from_playlist(request: Request) -> str:
    spotify = curator_logic.create_spotify()
    form = CuratorForm()
    if request.method == "GET":
        return render_template("curator_from_playlist.html", form=form)
    if request.method == "POST":
        # The request.form.get can retrieve the name of a form field
        # without needing to therefore use a wtf-form
        selected_playlist_id = request.form.get("selected_playlist_id")
        df = playlist_logic.get_tracks_df_from_playlist_id(selected_playlist_id)
        tracks = list(df["track_id"])
        recommended_tracks = curator_logic.get_sample_of_recommendation_from_tracks(
            spotify, tracks, 4
        )
        return render_template(
            "recommended_panel.html", track_recommendations=recommended_tracks
        )


def _curator_from_scratch(request: Request) -> str:
    spotify = curator_logic.create_spotify()
    form = CuratorForm()
    if request.method == "GET":
        return render_template("curator_from_scratch.html", form=form)
    if request.method == "POST":
        genre_select_result = form.genre_select.data
        recommended_tracks = curator_logic.get_multi_recommendation_tracks(
            spotify, genre_select_result
        )
        return render_template(
            "recommended_panel.html", track_recommendations=recommended_tracks
        )
