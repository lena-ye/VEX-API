import requests
import json
import os
from config import API_KEY, TEAM_NUMBER

base_url = "https://www.robotevents.com/api/v2/teams"
needed_parameters = [
    ("number[]", f"{TEAM_NUMBER}"),
]

my_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

all_teams = []

# Get current file path to save .json file in the current directory
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teams.json")


response = requests.get(base_url, params = needed_parameters, headers = my_headers)
print("Status Code:", response.status_code)


if response.status_code == 200:
    data = response.json()

    # Mehtod 1 - Output data directly to console

    # print(json.dumps(data, indent=4))


    # Method 2 - Save data to .json file

    # Check file path 
    # filepath = os.path.abspath("teams.json")
    # print(f"File saved to: {filepath}")

    # Write data into file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    

else:
    print("Request failed.")
    print("Response text:", response.text)
