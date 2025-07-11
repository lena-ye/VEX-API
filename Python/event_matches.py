# This program produces a .json file containing all matches at an event.

import requests
import json
import os
from config import *

def get_all_matches():
    div = 1; # MODIFY THIS PART for your needs
    base_url = f"https://www.robotevents.com/api/v2/events/{EVENT_ID}/divisions/{div}/matches" 
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config.py
    }
    all_matches = []
    page = 1
    per_page = 250

    while True:
        params = {
            "page": page,
            "per_page": per_page,
            "grade[]": ["College"] 
        }
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json() # data[] holds one page of results at a time

        # Condition to check if we've reached the end of all data
        if not data.get("data"):
            break

        all_matches.extend(data["data"])
        page += 1

    return all_matches

# Get all matches
matches = get_all_matches()

# Save to a JSON file in the same directory
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(__file__))[0] + ".json")
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=2) # for readability

print(f"Saved {len(matches)} matches to {file_path}")
