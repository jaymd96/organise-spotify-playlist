import spotipy
import os
from flask import session

spotify_scope = os.getenv("SPOTIFY_SCOPE")

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get("uuid")


class AuthHelper:
    def __init__(self):
        self.cache_handler = spotipy.cache_handler.CacheFileHandler(
            cache_path=session_cache_path()
        )
        self.auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=spotify_scope,
            cache_handler=self.cache_handler,
            show_dialog=True,
        )

    def get_access_token(self, code: str):
        return self.auth_manager.get_access_token(code)

    @property
    def validate_token(self):
        return self.auth_manager.validate_token(self.cache_handler.get_cached_token())

    @property
    def auth_url(self):
        return self.auth_manager.get_authorize_url()
