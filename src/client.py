import dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

env = dotenv.load_dotenv()

scope = ["user-library-read", "playlist-modify-private", "playlist-read-private"]
user = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_user_id(user):
    return user.me()["id"]
