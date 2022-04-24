import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from client import SpotifyClient
import uuid
import dotenv
import organise
import stats
import track
from flask_cors import CORS, cross_origin

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

jinja_env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape()
)

env = dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE")
app.config["SESSION_FILE_DIR"] = os.getenv("SESSION_FILE_DIR")
CORS(
    app,
)
Session(app)

spotify_scope = os.getenv("SPOTIFY_SCOPE")

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get("uuid")


@app.route("/callback/")
def callback():
    return redirect(f"/?{request.query_string.decode()}")


@app.route("/")
def index():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=spotify_scope,
        cache_handler=cache_handler,
        show_dialog=True,
    )

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # Step 4. Signed in, display data
    spotify = SpotifyClient(auth_manager=auth_manager)
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
    return redirect("http://localhost:3000/#/go")


@cross_origin()
@app.route("/playlist")
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


@app.route("/go")
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


@app.route("/sign_out")
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


@app.route("/current_user")
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = SpotifyClient(auth_manager=auth_manager)
    return spotify.current_user()


"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    app.run(
        threaded=True,
        port=int(os.environ.get("PORT", 8888)),
    )
