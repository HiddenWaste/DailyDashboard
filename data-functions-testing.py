import requests
import json
import pandas as pd

url = "https://genius-song-lyrics1.p.rapidapi.com/chart/artists/"

querystring = {"id": "2396871"}	# ID to retrive artist chart from Genius API

X_RAPIDAPI_KEY = "88d85341a3msh6a285814de5ffc0p10d2d5jsnd07b4d6f6f15"	# RapidAPI key Constant

headers = {
    "x-rapidapi-key": X_RAPIDAPI_KEY,	# RapidAPI key
    "x-rapidapi-host": "genius-song-lyrics1.p.rapidapi.com"					# RapidAPI host (Genius API)
}

response = requests.get(url, headers=headers, params=querystring)
response_json = response.json()

# Print the entire response JSON for debugging
print(json.dumps(response_json, indent=4))

# Initialize an empty list to store the filtered artist information
artist_list = []

# Define the names of artists to filter out
artists_to_filter = {"Genius Romanizations", "Genius English Translations", "Genius Traducciones al Español"}

# Extract artist details from the response
for chart_item in response_json.get('chart_items', []):
    artist = chart_item.get('item', {})
    
    artist_info = {
        "name": artist.get('name'),
        "header_image_url": artist.get('header_image_url'),
        "url": artist.get('url')
    }
    # Only add artist to the list if their name is not in the filter list
    if artist_info['name'] not in artists_to_filter:
        artist_list.append(artist_info)

i = 0 # Artist rank iterator

# Print the filtered artist list
for artist in artist_list:
    # Print details for debugging
    print(f"Rank: {i+1}")										# Rank of the artist
    print(f"Name: {artist['name']}")							# Name of the artist
    print(f"Header Image URL: {artist['header_image_url']}")	# URL of the artist's header image
    print(f"URL: {artist['url']}")								# URL of the artist's Genius page
    print("\n")													# Newline for separation		
    i += 1														# Increment the rank iterator

# Create a DataFrame from the artist list
artist_df = pd.DataFrame(artist_list)
print(artist_df)

# Optionally save the artist list to a json file
with open('artist_charts.json', 'w') as file:
    json.dump(artist_list, file, indent=4)
