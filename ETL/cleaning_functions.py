import json
import pandas as pd

# import spotipy
# import spotipy.util as util


# with open('../credentials.json') as filename:
#     credentials = json.load(filename)
#     filename.close()
    
# token = util.oauth2.SpotifyClientCredentials(client_id=credentials['client_id'],
#                                              client_secret=credentials['client_secret'])
# ## creates an access token for you to do what you need to do
# cache_token = token.get_access_token()
# sp = spotipy.Spotify(cache_token)


def _clean_search_results(results):
    meta= results[0]
    keys = ['artists', 'duration_ms', 'explicit', 'name', 'uri', 'release_date']
    meta_dict = {}
    for key in keys:
        if key == 'artists':
            meta_dict[key] = ', '.join([artist['name'] for artist in meta[key]])
        elif key == 'release_date':
            meta_dict[key] = meta['album']['release_date']

        else: meta_dict[key] = meta[key]
    return meta_dict

def get_features(df, sp):
    results_list = []
    for queries in df.search_queries.values:
        test = sp.search(q=queries, type = 'track', limit=1)
        try:
            results = test['tracks']['items']
            cleaned = _clean_search_results(results) # returns a dictionary
        except:
            cleaned = {}
        cleaned['search_query'] = queries
        results_list.append(cleaned)
    yield list(results_list)
    
def get_audio_features(id_value, sp):
    '''
    pass in the song's uri id string , and through the audiofeautes endpoint it returns the data there in a dictionary
    '''
    try:
        results = sp.audio_features(id_value)[0]
        results['id'] = id_value
    except Exception as e:
        results = {}
        results['id'] = 'missing'
    return results



def get_audio_analysis(song_id, sp):
    """
    takes the song id and passes it through the spotify api to get the song analysis values
    and if there is no song_id then it passes and returns an empty string
    """
    relevant_columns = ['num_samples', 'duration', 'sample_md5', 'offset_seconds',
                             'window_seconds', 'analysis_sample_rate', 'analysis_channels',
                             'end_of_fade_in', 'start_of_fade_out', 'loudness', 'tempo',
                             'tempo_confidence', 'time_signature', 'time_signature_confidence',
                             'key', 'key_confidence', 'mode', 'mode_confidence']
    try:
        song_analysis = sp.audio_analysis(song_id)['track']
        result = {key:song_analysis[key] for key in song_analysis if key in relevant_columns}
    except Exception as e:
        print(e)
        result = {key:'' for key in relevant_columns}
    result['id'] = song_id
    return result
        
    
def get_best_results(query, results):
    '''i should create a function that compares the search name to the result name and return the results that are the highest match
    and then from there i need to get all the necessary things from the api
    '''
    match_ratio = []
    for index, result in enumerate(results['artists']['items']):
        match_ratio.append((index,
                                 fuzz.ratio(query, result['name'])))
    best_result_index = sorted(match_ratio, key=lambda x: x[1], reverse=True)[0][0]
    features = ['id', 'name', 'popularity', 'genres'] # missing followers
    best_result = results['artists']['items'][best_result_index]
    best_result_dict = {}
    for feature in features:
        best_result_dict[feature] = best_result[feature]
    best_result_dict['followers'] = best_result['followers']['total']
    best_result_dict['query'] = query
    return best_result_dict