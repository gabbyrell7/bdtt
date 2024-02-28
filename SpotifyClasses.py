import csv

class Song:
    def __init__(self, artist_name, track_name, album_name, release_year, duration_minutes, duration_seconds, popularity, track_id):
        self.artist_name = artist_name
        self.track_name = track_name
        self.album_name = album_name
        self.release_year = release_year
        self.duration_minutes = duration_minutes
        self.duration_seconds = duration_seconds
        self.popularity = popularity
        self.track_id = track_id

class Playlist:
    def __init__(self, playlist_id, songs):
        self.playlist_id = playlist_id
        self.songs = songs

    def get_spotify_playlist(self):
        # List to store Track objects
        tracks = []

        # Access information about each track in the playlist
        popularity_values = [track['track']['popularity'] for track in self.songs['items']]

        # Calculate the average popularity (excluding tracks with popularity 0)
        non_zero_popularities = [pop for pop in popularity_values if pop != 0]
        average_popularity = round(sum(non_zero_popularities) / len(non_zero_popularities)) if non_zero_popularities else 0

        # Iterate through each track
        for track_data in self.songs['items']:
            # Extract data for each track
            popularity = track_data['track']['popularity']
            
            # If popularity is 0, replace it with the average popularity
            if popularity == 0:
                popularity = average_popularity

            track = Song(
                artist_name=track_data['track']['artists'][0]['name'],
                track_name=track_data['track']['name'],
                album_name=track_data['track']['album']['name'],
                release_year=track_data['track']['album']['release_date'].split('-')[0],
                duration_minutes=track_data['track']['duration_ms'] // 60000,
                duration_seconds=(track_data['track']['duration_ms'] // 1000) % 60,
                popularity=popularity,
                track_id=track_data['track']['id']
            )

            # Append the Track object to the list
            tracks.append(track)

        print(f"This playlist has {len(tracks)} songs.")

        return tracks