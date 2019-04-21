def get_artist_name(search_result):
    '''
    only looks at the first item of the search result since that would be the highest probability of matching
    the search query

    if there are multiple artists on the song, it will iterate through it and return a string of the artist(s)
    '''
    return ', '.join([item['name'] for item in search_result[0]['artists']])

def clean_search_results(search_results):
    '''
    will take the result from the search query and clean it to extract the essential information and return a dictionary
    '''
    results_dict = {}
    if len(search_results) > 0:
        results_dict['id'] = search_results[0]['id']
        results_dict['name'] = search_results[0]['name']
        results_dict['artists'] = get_artist_name(search_results)
        results_dict['popularity'] = search_results[0]['popularity']
        results_dict['explicit'] = search_results[0]['explicit']
        results_dict['duration_ms'] = search_results[0]['duration_ms']
    else:
        results_dict['id'] = ''
        results_dict['name'] = ''
        results_dict['artists'] = ''
        results_dict['popularity'] = ''
        results_dict['explicit'] = ''
        results_dict['duration_ms'] = ''
    return results_dict
