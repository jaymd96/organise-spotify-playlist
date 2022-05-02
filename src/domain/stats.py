from operator import add
import toolz

ms_in_hr = 3600000


def _calc_duration(tracks):
    return toolz.reduce(
        add,
        toolz.pluck(
            "duration_ms",
            toolz.map(vars, tracks),
        ),
    )


def oragnised_stats(organised_tracks):
    return {
        "summary": {
            "tracks": toolz.count(toolz.concat(organised_tracks.values())),
            "playlists": len(organised_tracks.keys()),
            "hours": _calc_duration(toolz.concat(organised_tracks.values()))
            // ms_in_hr,
        },
        "playlists": [
            {
                "name": playlist[0],
                "tracks": toolz.count(playlist[1]),
                "hours": round(_calc_duration(playlist[1]) / ms_in_hr, 1),
            }
            for playlist in organised_tracks.items()
        ],
    }
