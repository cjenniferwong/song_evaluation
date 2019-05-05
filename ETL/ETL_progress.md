## Here is how the data was collected, and generated:
1. list of songs scraped from billboards top 100 charts, and the number of weeks calculated for each song
    - data stored in billboards.csv
2. create a search query, and use the spotify api to get search results and the corresponding song uri that best matches it
    - note that some songs required manually modifying the search query in order to get any result
    - final data stored in spotify_search.pkl