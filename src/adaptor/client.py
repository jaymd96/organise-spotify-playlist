import dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

env = dotenv.load_dotenv()

scope = ["user-library-read", "playlist-modify-private", "playlist-read-private"]


class SpotifyClient(spotipy.Spotify):
    @property
    def user_id(self):
        return self.me()["id"]


user = SpotifyClient(auth_manager=SpotifyOAuth(scope=scope))
