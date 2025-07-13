# Gets information about one event using its SKU, which is a unique event identifier that can
#   be easily found on the registration page at robotevents.com

import requests
import json
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from config import *

# Set up
base_url = "https://www.robotevents.com/api/v2/events"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config.py
}

params = {
    "sku[]": "RE-V5RC-25-0299",
}

# Get response
response = requests.get(base_url, headers=headers, params=params)
print("Status Code:", response.status_code)

response.raise_for_status()


if response.status_code == 200:
    data = response.json()
    
    # Write data into file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(__file__))[0] + ".json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    

else:
    print("Request failed.")
    print("Response text:", response.text)

