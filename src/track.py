import model
from typing import List


Track = model.TrackObject
Tracks = List[Track]
PlaylistTrack = model.PlaylistTrackObject
PlaylistTracks = List[PlaylistTrack]
Playlist = model.SimplifiedPlaylistObject
Playlists = List[Playlist]


def _spotify_pagination_helper(cls, paginated_call, limit_step, max_offset):
    pages = []
    for offset in range(0, max_offset, limit_step):
        raw_page = paginated_call(limit=limit_step, offset=offset)
        page = cls(**raw_page)
        if len(page.items) == 0:
            break
        pages.extend(page.items)
    return pages


def get_all_saved_tracks(client, limit_step=50, max_offset=5000) -> Tracks:
    return _spotify_pagination_helper(
        cls=model.PlaylistTracksPagingObject,
        paginated_call=client.current_user_saved_tracks,
        limit_step=limit_step,
        max_offset=max_offset,
    )


def get_all_playlists(client, limit_step=50, max_offset=500) -> Playlists:
    return _spotify_pagination_helper(
        cls=model.PlaylistsPagingObject,
        paginated_call=client.current_user_playlists,
        limit_step=limit_step,
        max_offset=max_offset,
    )
