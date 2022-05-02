import spotipy
import os
from flask import session

spotify_scope = os.getenv("SPOTIFY_SCOPE")

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get("uuid")


class SpotipyAuth(spotipy.oauth2.SpotifyOAuth):
    def __init__(
        self,
    ):
        super().__init__(
            scope=spotify_scope,
            cache_handler=spotipy.cache_handler.CacheFileHandler(
                cache_path=session_cache_path()
            ),
            show_dialog=True,
        )

    @property
    def has_token(self):
        return self.validate_token(self.cache_handler.get_cached_token()) != None

    @property
    def auth_url(self):
        return self.get_authorize_url()
