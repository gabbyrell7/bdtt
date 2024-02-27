# spotify_app

**Create a Spotify Developer Account for the API**
- Go to [https://developer.spotify.com/](https://developer.spotify.com/) to create one.
- Create an App
- Note: set your Redirect URIs to http://localhost and use your app as a Web API.
- Go to your apps settings to locate your Client ID and Client Secret

**Setup**
- Create a new folder (Example: spotify_app) in your machine

```
git clone https://github.com/gabbyrell7/spotify_app.git
cd spotify_app
```

- pip install spotipy
- Rename config_template.yaml to config.yaml
- Substitute it with your Spotify Developer and Redis details.
- Open VSCode and open spotify_app folder.

**Run the Application**
```
spotify_app> python3 ./main.py
```
