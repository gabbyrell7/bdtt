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

    def __str__(self):
        return f"{self.artist_name} - {self.track_name} ({self.release_year})"


class Playlist:
    def __init__(self, playlist_id, tracks):
        self.playlist_id = playlist_id
        self.tracks = tracks

    def add_track(self, track):
        self.tracks.append(track)

    def __str__(self):
        return f"Playlist with {len(self.tracks)} songs."

    @classmethod
    def get_spotify_playlist(cls, playlist_id, playlist_tracks):
        # List to store Track objects
        tracks = []

        # Access information about each track in the playlist
        popularity_values = [track['track']['popularity'] for track in playlist_tracks['items']]

        # Calculate the average popularity (excluding tracks with popularity 0)
        non_zero_popularities = [pop for pop in popularity_values if pop != 0]
        average_popularity = round(sum(non_zero_popularities) / len(non_zero_popularities)) if non_zero_popularities else 0

        # Iterate through each track
        for track_data in playlist_tracks['items']:
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

        playlist_instance = cls(playlist_id, tracks)

        return playlist_instance
    
    @classmethod
    def playlist_to_cvs(cls, my_playlist):
        # Extract songs from the Playlist instance
        tracks = my_playlist.tracks

        # Define the CSV file path
        csv_file_path = 'spotify_data.csv'

        # Write the list of dictionaries to the CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            if tracks:
                fieldnames = tracks[0].__dict__.keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header
                writer.writeheader()

                # Write the data
                for track in tracks:
                    writer.writerow(track.__dict__)

                print(f'Playlist data has been successfully exported to "{csv_file_path}"')
            else:
                print('Playlist is empty, cannot export to CSV.')