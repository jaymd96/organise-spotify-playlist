import toolz


def oragnised_stats(organised_tracks):
    return {
        "total_track_count": toolz.count(toolz.concat(organised_tracks.values())),
        "total_playlist_count": len(organised_tracks.keys()),
        "playlist_count": toolz.valmap(len, organised_tracks),
    }
