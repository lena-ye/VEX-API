import requests
import json
import os
import time
from collections import defaultdict
from config_interactive import *


# ====================================================================
# Step [] - Get info about a team 
# template: team.py
# ====================================================================

print(f"Getting info about team: {TEAM_NUMBER}")

base_url = "https://www.robotevents.com/api/v2/teams"
needed_parameters = [
    ("number[]", f"{TEAM_NUMBER}"), # add TEAM_NUMBER="..." to config_interactive.py
]

my_headers = {
    "Authorization": f"Bearer {API_KEY}", # add API_KEY="..." to config_interactive.py
    "Accept": "application/json"
}

# Save .json file in the current directory
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "team.json")

# Make the request
response = requests.get(base_url, params=needed_parameters, headers=my_headers)
print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    # Save data to .json file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Data saved to {file_path}")

else:
    print("Request failed.")
    print("Response text:", response.text)

# Get TEAM_ID from event.json generated.
TEAM_ID = data["data"][0]["id"]
print(f"TEAM_ID: {TEAM_ID}")

print()

# ====================================================================
# Step [] - Get info about the event 
# template: event_Worlds.py
# ====================================================================

print(f"Getting info about event with SKU: {EVENT_SKU}")

base_url = "https://www.robotevents.com/api/v2/events"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

params = {
    "sku[]": f"{EVENT_SKU}"
}

# Get response
response = requests.get(base_url, headers=headers, params=params)
print("Status Code:", response.status_code)

response.raise_for_status()


if response.status_code == 200:
    data = response.json()
    
    # Write data into file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {file_path}")

else:
    print("Request failed.")
    print("Response text:", response.text)

print()



# ====================================================================
# Step [] - Invite user to select division 
# ====================================================================

# Load data
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event.json")

# Wait up to 2 seconds for file to appear
for _ in range(2):
    if os.path.exists(json_path):
        break
    time.sleep(1)
else:
    print("File 'event.json' not found after waiting.")
    exit()

# Open file for processing
try:
    with open(f"{json_path}", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("File 'event.json' not found.")
    exit()
except json.JSONDecodeError:
    print("Failed to decode JSON from 'event.json'. Is the file valid?")
    exit()

# Extract the event and its divisions
event = data["data"][0]
divisions = event.get("divisions", [])

if not divisions:
    print("No divisions found for this event.")
    exit()

print("Available Divisions:")
for division in divisions:
    print(f"ID: {division['id']}, Name: {division['name']}")

# Prompt user to select their division of interest
user_input = input("\nEnter the division ID you're interested in: ").strip()

try:
    selected_id = int(user_input)
except ValueError:
    print("Invalid input. Please enter a single numeric ID.")
    exit()

# Validate the selected ID
valid_ids = {div["id"] for div in divisions}
if selected_id not in valid_ids:
    print("Invalid division ID selected.")
    exit()

print(f"Selected division ID: {selected_id}")
DIVISION_ID = selected_id

print()

# ====================================================================
# Step [] - Get list of teams in the event 
# template: event_matches.py
# ====================================================================

# Get EVENT_ID from event.json generated in Step 2.
# This is required to get the list of participating teams at the event
EVENT_ID = data["data"][0]["id"]


def get_all_matches():
    base_url = f"https://www.robotevents.com/api/v2/events/{EVENT_ID}/divisions/{DIVISION_ID}/matches" 
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
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event_matches.json")
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=2) # for readability

print(f"Saved {len(matches)} matches to {file_path}")
print()


# ====================================================================
# Step [] - Get list of teams by division 
# ====================================================================

# When scouting for Qualification Matches, we are only interested in the teams in our division.
# This has to be done via event matches because it is the only instance where team numbers
#     are associated with team divisions. 

json_path = file_path
# Load the JSON file
try:
    with open(json_path, "r") as f:
        matches = json.load(f)
except Exception as e:
    print(f"Failed to load JSON: {e}")
    exit()

# Map of division_id → set of unique team names
teams_by_division_id = defaultdict(set)

# Process each match
for match in matches:
    division_id = match["division"]["id"]
    alliances = match.get("alliances", [])
    for alliance in alliances:
        for team_entry in alliance.get("teams", []):
            team_name = team_entry["team"]["name"]
            teams_by_division_id[division_id].add(team_name)

# Display results
for division_id, team_names in teams_by_division_id.items():
    print(f"In Division {division_id}:")
    for name in sorted(team_names):
        print(f"{name}")


# ====================================================================
# Step [] - For each team, find all events they've been to. (events_attended.py)
# For each of their events, get the team's wp, Qualification Matches, 
# (event_matches.py) calculate statistics, and store info in an array.
# template: events_attended.py, event_matches.py
# ====================================================================


"""
Here's the situation:
A team participates in several tournaments each year. The number varies by team. 
The team participates in a number of Qualification Matches at the tournament. That number also varies by tournament. 
They will get 0, 1, or 2 autonomous win points in each match. 
We want to compare the teams based on their points which reflect their skill level.

How do we standardize the measure? The following is what we will use:
average ap per match = P / M
where:
- P is calculated as sum of (wp - 2 * number of Qualification Matches won in a specific tournament)
- M is the total number of matches they've competed in so far

Pseudocode:
for each team:
    total_awp = 0
    total_matches = 0

    for each tournament
        matches_won = 0
        [parse .json ...]
        get the number of Qs the team competed in. + to total_matches
        if team score > opponent score, +1 to matches_won.

        get rankings, which will tell us the team's wp.
        awp = wp - 2 * matches_won
        total_awp += awp
    
    avg_awp = total_awp / total_matches
    store [team number, total_awp, total_matches, avg_awp]
"""

