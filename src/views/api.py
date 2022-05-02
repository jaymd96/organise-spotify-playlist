import os
import uuid

from flask import session, request, redirect, Blueprint
from flask_cors import cross_origin
import spotipy

from adaptor.client import SpotifyClient
from adaptor.auth import session_cache_path, SpotipyAuth

import domain.organise
import domain.stats
import domain.track

import views.web as web

api_bp = Blueprint(name="api-bp", import_name=__name__, url_prefix="/api")


@cross_origin()
@api_bp.route("/callback/")
def callback():
    return redirect(f"/api?{request.query_string.decode()}")


@api_bp.route("/")
def index():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        session["uuid"] = str(uuid.uuid4())

    auth_manager = SpotipyAuth()

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return web.redirect("/index.html#/go")

    if not auth_manager.has_token:
        # Step 2. Display sign in link when no token
        return redirect(auth_manager.auth_url)

    return web.redirect("/index.html#/go")


@cross_origin()
@api_bp.route("/playlist")
def preview_playlists():

    auth_manager = SpotipyAuth()

    if not auth_manager.has_token:
        # Step 2. Display sign in link when no token
        return redirect(auth_manager.auth_url)

    spotify = SpotifyClient(auth_manager=auth_manager)

    return {
        "profile": {
            "name": spotify.user_name,
            "picture": spotify.user_image,
        },
        **domain.stats.oragnised_stats(
            domain.organise.organise_playlist_by_year_month(
                domain.organise.get_all_saved_tracks(spotify)
            )
        ),
    }


@api_bp.route("/playlist", methods=["PUT"])
def make_playlists():

    auth_manager = SpotipyAuth()

    if not auth_manager.has_token:
        # Step 2. Display sign in link when no token
        return redirect(auth_manager.auth_url)

    spotify = SpotifyClient(auth_manager=auth_manager)
    domain.organise.make_playlists(
        spotify, domain.organise.organise_playlist_by_year_month
    )


@api_bp.route("/sign_out")
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")
