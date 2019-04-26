import spotipy
import spotipy.util as util
import json

with open('credentials.json') as filename:
    credentials = json.load(filename)
    filename.close()
    
class Spotify(client_id = credentials['client_id'], client_secret = credentials['client_secret']):
    def __init__(self, name, age):
        self.client_id = client_id
        self.client_secret = client_secret
        
    token = util.oauth2.SpotifyClientCredentials(client_id=credentials['client_id'],
                                             client_secret=credentials['client_secret'])
    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)
    return sp