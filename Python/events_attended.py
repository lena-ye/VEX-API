# Obtains a list of events a team has attended in the specified time frame

# Imports
import requests
import json
import os
from config import * # you need to create a config.py file 

base_url = f"https://www.robotevents.com/api/v2/teams/{TEAM_ID}/events"
needed_parameters = { # make sure you have the following in config.py
    "id[]" : f"{TEAM_ID}", 
    "start" : f"{START_DATE}",
    "end" : f"{END_DATE}",
}

my_headers = {
    "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config.py
    "Accept": "application/json"
}


# Get current file path to save .json file in the current directory
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(__file__))[0] + ".json")

response = requests.get(base_url, params = needed_parameters, headers = my_headers)
print("Status Code:", response.status_code)


if response.status_code == 200:
    data = response.json()

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {file_path}.")

else:
    print("Request failed.")
    print("Response text:", response.text)
