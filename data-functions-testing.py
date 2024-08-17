import requests
import json

url = "https://genius-song-lyrics1.p.rapidapi.com/chart/artists/"

querystring = {"id":"2396871"}

headers = {
	"x-rapidapi-key": "88d85341a3msh6a285814de5ffc0p10d2d5jsnd07b4d6f6f15",
	"x-rapidapi-host": "genius-song-lyrics1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# Format the json response by taking out unecessary data and indenting
json_data = json.dumps(response.json(), indent=4)
# Save the response to a file
with open('artist_charts.json', 'w') as file:
	json.dump(response.json(), file, indent=4)
