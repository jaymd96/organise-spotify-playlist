import organise
import client

if __name__ == "__main__":
    organise.make_playlists(client.user, organise.organise_playlist_by_year_month)
