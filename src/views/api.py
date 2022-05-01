import os
import uuid

from flask import session, request, redirect, Blueprint
from flask_cors import cross_origin
import spotipy

from client import SpotifyClient
from auth import AuthHelper, session_cache_path, spotify_scope
import organise
import stats
import track

api_bp = Blueprint(name="api-bp", import_name=__name__, url_prefix="/api")


@cross_origin()
@api_bp.route("/callback/")
def callback():
    print(request.url_rule.rule)
    return redirect(f"/api?{request.query_string.decode()}")


@api_bp.route("/")
def index():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        session["uuid"] = str(uuid.uuid4())

    auth_manager = AuthHelper()

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect("/index.html#/go")

    if not auth_manager.validate_token:
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.auth_url
        return redirect(auth_url)

    # Step 4. Signed in, display data
    spotify = SpotifyClient(auth_manager=auth_manager.auth_manager)
    params = {
        "name": spotify.me()["display_name"],
        "picture": "https://i.pinimg.com/originals/a8/bc/90/a8bc90ea196737604770aaf9c2d56a51.jpg",
    }
    params = {
        **params,
        **stats.oragnised_stats(
            organise.organise_playlist_by_year_month(
                track.get_all_saved_tracks(spotify)
            )
        ),
    }
    return redirect("/index.html#/go")


@cross_origin()
@api_bp.route("/playlist")
def preview_playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=spotify_scope,
        cache_handler=cache_handler,
        show_dialog=True,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    spotify = SpotifyClient(auth_manager=auth_manager)
    return {
        "profile": {
            "name": spotify.me()["display_name"],
            "picture": spotify.me()["images"][-1]["url"],
        },
        **stats.oragnised_stats(
            organise.organise_playlist_by_year_month(
                organise.get_all_saved_tracks(spotify)
            )
        ),
    }


@api_bp.route("/go")
def make_playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=spotify_scope,
        cache_handler=cache_handler,
        show_dialog=True,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    spotify = SpotifyClient(auth_manager=auth_manager)
    organise.make_playlists(spotify, organise.organise_playlist_by_year_month)
    return f"<h1>playlists organised</h1>"


@api_bp.route("/sign_out")
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


@api_bp.route("/current_user")
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = SpotifyClient(auth_manager=auth_manager)
    return spotify.current_user()
