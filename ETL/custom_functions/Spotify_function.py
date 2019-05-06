import spotipy
import spotipy.util as util
import json

def Spotify_func(json_file = "credentials.json"):
    with open(json_file) as filename:
        credentials = json.load(filename)
        filename.close()
        
    token = util.oauth2.SpotifyClientCredentials(client_id=credentials['client_id'],
                                             client_secret=credentials['client_secret'])
    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)
    return sp