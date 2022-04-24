import organise
import client
import stats
from pprint import pprint

if __name__ == "__main__":

    stats = stats.oragnised_stats(
        organise.organise_playlist_by_year_month(
            organise.get_all_saved_tracks(client.user)
        )
    )
