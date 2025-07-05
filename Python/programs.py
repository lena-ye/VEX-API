import requests
import json
import os
from config import API_KEY, TEAM_NUMBER # you need to create a config.py file 

base_url = "https://www.robotevents.com/api/v2/programs" 


my_headers = {
    "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config.py
    "Accept": "application/json"
}

params = {
    "id[]" : ""
}


# Get current file path to save .json file in the current directory
script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{script_name}.json")


response = requests.get(base_url, headers = my_headers)
print("Status Code:", response.status_code)


if response.status_code == 200:
    data = response.json()

    # Write data into file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    

else:
    print("Request failed.")
    print("Response text:", response.text)
