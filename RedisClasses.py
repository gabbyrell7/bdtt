import pandas as pd
import redis
import json

class RedisFuncs:
    def __init__(self, redis_connection):
        self.r = redis_connection

    def store_playlist_in_redis(self, key_prefix, songs):
        # Store data into Redis
        for index, song in enumerate(songs):
            # Using the index as part of the key
            key = f"{key_prefix}:{index}"
            # Convert row to a dict and store in Redis
            self.store_json_in_redis(key, song.__dict__)

        print(f"Inserted data into Redis with key {key_prefix}")

    def store_json_in_redis(self, key, data):
        # Convert the data to JSON and store in Redis
        json_data = json.dumps(data)
        self.r.json().set(key, ".", json_data)

    def songs_release_year(self, start, end):
        keys = self.r.keys("songs:*")
        
        filtered_songs = []
        for key in keys:
            json_data = self.r.json().get(key)
            song_data = json.loads(json_data)
            
            # Check if the release year is between specific years
            release_year = int(song_data.get("release_year", 0))
            if start <= release_year <= end:
                filtered_songs.append(song_data)

        print(f"There were {len(filtered_songs)} Songs released between the years 1985 and 1995.")

    def most_popular_song(self):
        keys = self.r.keys("songs:*")

        # Initialize variables to track the maximum popularity and the corresponding key
        max_popularity = float('-inf')  # Initialize with negative infinity
        key_with_max_popularity = None

        # Iterate through keys and find the one with the maximum popularity
        for key in keys:
            json_data = self.r.json().get(key)
            song_data = json.loads(json_data)
            popularity = float(song_data.get('popularity', 0))
            if popularity > max_popularity:
                max_popularity = popularity
                key_with_max_popularity = key

        track = song_data.get('track_name')
        artist = song_data.get('artist_name')

        print(f"Key with the most popularity: {key_with_max_popularity}.")
        print(f"This is {track} by {artist}.")

    def convert_to_pd_df(self):
        keys = self.r.keys("songs:*")

        # Retrieve and convert data to a pandas DataFrame
        data = []
        for key in keys:
            json_data = self.r.json().get(key)
            data.append(json.loads(json_data))

        columns_to_include = ["artist_name", "track_name", "album_name", "release_year", "duration_minutes", "duration_seconds", "popularity", "track_id"]

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)[columns_to_include]

        return df    
