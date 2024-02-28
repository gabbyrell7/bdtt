import pandas as pd
from SpotifyClasses import *
from RedisClasses import *
from PlotOps import *
from db_config import get_spotify_connection, get_redis_connection

if __name__ == "__main__":

    # Authenticate with Spotify API.
    sp = get_spotify_connection()

    # Playlist ID for the desired playlist and get playlist songs.
    playlist_id = '3rK8myfHsDIAiMBueb1k38'
    playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id)

    # Create Playlist instance and print the information
    my_playlist_instance = Playlist(playlist_id, playlist_tracks)
    my_playlist = my_playlist_instance.get_spotify_playlist()

    # Connect to redis
    r = get_redis_connection()

    # Create and instance of RedisFuncs
    redis_funcs = RedisFuncs(r)

    # Insert data into Redis
    redis_funcs.store_playlist_in_redis("songs", my_playlist)

    # Use Redis to find number of songs released between specific years
    redis_funcs.songs_release_year(1985, 1995)

    # Use Redis to find the most popular songs key and track name and artist
    redis_funcs.most_popular_song()

    # Convert Redis data to pandas dataframe
    df = redis_funcs.convert_to_pd_df()

    plots = PlotOps(df)

    # Graph total of songs released each year
    plots.graph_songs_per_year()

    # Graph top 10 Songs based on Popularity
    plots.graph_top_10_songs()






