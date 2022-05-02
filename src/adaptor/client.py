import dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

env = dotenv.load_dotenv()

scope = ["user-library-read", "playlist-modify-private", "playlist-read-private"]


class SpotifyClient(spotipy.Spotify):
    @property
    def user_id(self):
        return self.me()["id"]

    @property
    def user_name(self):
        return self.me()["display_name"]

    @property
    def user_image(self):
        try:
            image = self.me()["images"][-1]["url"]
        except IndexError:
            image = "https://i.pinimg.com/originals/a8/bc/90/a8bc90ea196737604770aaf9c2d56a51.jpg"
        return image
