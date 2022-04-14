import client
import toolz
from track import (
    get_all_saved_tracks,
    get_all_playlists,
)
import model
import functools

###
# HELPERS
###
def _year_month(playlist_track):
    return playlist_track.added_at.strftime("%Y-%m")


def _groupby(tracklike, key):
    return toolz.groupby(key, tracklike)


def _organise(tracklike, key, proj_fn):
    return toolz.valmap(
        lambda eles: [proj_fn(ele) for ele in eles], _groupby(tracklike, key)
    )


def search_existing_playlist(existing_playlist, candidate_name):
    return next(
        filter(lambda p: p.name == candidate_name, existing_playlist),
        False,
    )


###
# ORANGISER
###
organise_playlist_by_year_month = functools.partial(
    _organise, key=_year_month, proj_fn=lambda plt: plt.track
)


def make_playlists(client, organiser):
    user_playlists = get_all_playlists(client.user)
    grouped_tracks = organiser(get_all_saved_tracks(client.user))

    for playlist_name, tracks in grouped_tracks.items():
        if search_existing_playlist(user_playlists, playlist_name):
            playlist = search_existing_playlist(user_playlists, playlist_name)
        else:
            playlist_response = client.user.user_playlist_create(
                client.get_user_id(client.user),
                playlist_name,
                public=False,
                collaborative=False,
                description=f"Playlist with all the songs liked on {playlist_name}",
            )
            playlist = model.PlaylistObject(**playlist_response)

        track_ids = [t.id for t in tracks]
        client.user.user_playlist_replace_tracks(
            client.get_user_id(client.user), playlist.id, track_ids
        )
