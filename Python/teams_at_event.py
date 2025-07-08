import requests
import json
import os
from config import *

def get_all_teams():
    base_url = f"https://www.robotevents.com/api/v2/events/{EVENT_ID}/teams" 
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config.py
    }
    params = {
        "id" : f"{EVENT_ID}"
    }
    all_teams = []
    page = 1
    per_page = 250

    while True:
        params = {
            "page": page,
            "per_page": per_page,
        }
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json() # data[] holds one page of results at a time

        # Condition to check if we've reached the end of all data
        if not data.get("data"):
            break

        all_teams.extend(data["data"])
        page += 1

    return all_teams

# Get all teams
teams = get_all_teams()

# Save to a JSON file in the same directory
script_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{script_name}.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(teams, f, ensure_ascii=False, indent=2) # for readability

print(f"Saved {len(teams)} teams to {file_path}.")
