import pandas as pd
import redis

class RedisFuncs:
    def __init__(self, redis_connection):
        self.r = redis_connection
        RedisFuncs.r = redis_connection

    @classmethod
    def store_csv_in_redis(cls, file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ingest data into Redis
        for index, row in df.iterrows():
            # Using the index as part of the key
            key = f"songs:{index}"
            # Convert row to a dict and store in Redis
            cls.r.hset(key, mapping=row.to_dict())

        print(f"Inserted data into Redis with key songs")

    @classmethod
    def songs_release_year(cls, start, end):
        keys = cls.r.keys("songs:*")
        
        filtered_songs = []
        for key in keys:
            song_data = cls.r.hgetall(key)
            
            # Check if the release year is between specific years
            release_year = int(song_data.get("release_year", 0))
            if start <= release_year <= end:
                filtered_songs.append(song_data)

        print(f"There were {len(filtered_songs)} Songs released between the years 1985 and 1995.")

    @classmethod
    def most_popular_song(cls):
        keys = cls.r.keys("songs:*")

        # Initialize variables to track the maximum popularity and the corresponding key
        max_popularity = float('-inf')  # Initialize with negative infinity
        key_with_max_popularity = None

        # Iterate through keys and find the one with the maximum popularity
        for key in keys:
            popularity = float(cls.r.hget(key, 'popularity') or 0)
            if popularity > max_popularity:
                max_popularity = popularity
                key_with_max_popularity = key

        track = cls.r.hget(key_with_max_popularity, 'track_name')
        artist = cls.r.hget(key_with_max_popularity, 'artist_name')

        print(f"Key with the most popularity: {key_with_max_popularity}.")
        print(f"This is {track} by {artist}.")

    @classmethod
    def convert_to_pd_df(cls):
        keys = cls.r.keys("songs:*")

        # Retrieve and convert data to a pandas DataFrame
        data = []
        for key in keys:
            data.append(cls.r.hgetall(key))

        columns_to_include = ["artist_name", "track_name", "album_name", "release_year", "duration_minutes", "duration_seconds", "popularity", "track_id"]

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)[columns_to_include]

        return df    
