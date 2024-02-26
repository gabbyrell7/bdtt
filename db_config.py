import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import redis
import yaml

def load_config():
    """Load configuration from the YAML file.

    Returns:
        dict: Configuration data.
    """
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


config = load_config()

def get_spotify_connection():
    """Create a Spotify connection using Spotipy API.
    
    Returns:
        Spotify: Spotify connection object.
    """
    client_credentials_manager = SpotifyClientCredentials(client_id=config["spotify"]["cid"], 
                                                          client_secret=config["spotify"]["secret"])

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_redis_connection():
    """Create a Redis connection using the configuration.

    Returns:
        Redis: Redis connection object.
    """
    return redis.Redis(
        host=config["redis"]["host"],
        port=config["redis"]["port"],
        db=0,
        decode_responses=True,
        username=config["redis"]["user"],
        password=config["redis"]["password"],
    )

