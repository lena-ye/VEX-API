import requests
import json
import os
import time
import re
import plotly.graph_objects as go
import plotly.offline as pyo # to save bar graph
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
    print("Request for team info failed.")

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
    print("Request for event info failed.")

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
    time.sleep(0.1)
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
            team_id = team_entry["team"]["id"]
            teams_by_division_id[division_id].add((team_name, team_id))

# Display results
for division_id, team_info_set  in teams_by_division_id.items():
    print(f"In Division {division_id}:")
    for team_name, team_id in sorted(team_info_set):
        print(f"{team_name}") 

# print(teams_by_division_id)

# ====================================================================
# Step [] - For each team, find all events they've been to. (events_attended.py)
# For each of their events, get the team's wp, Qualification Matches, 
# (event_matches.py) calculate statistics, and store info in an array.
# template: events_attended.py, event_matches.py
# ====================================================================



"""
Here's the situation:
A team participates in several tournaments each year. The number varies by team. 
At each tournament, the team participates in a number of Qualification Matches. That number also varies by tournament. 
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
        if team score > opponent score, +1 to matches_won. (there's an easier way from rankings json response)

        get rankings, which will tell us the team's wp.
        awp = wp - 2 * matches_won
        total_awp += awp
    
    if total_matches != 0, avg_awp = total_awp / total_matches
    store [team number, total_awp, total_matches, avg_awp]
"""

team_stats = {}
for division_id, team_set in teams_by_division_id.items():
    for team_name, team_id in team_set:
        total_awp = 0
        total_matches = 0
        # First we get events attended 

        # print(f"team_id {team_id}")
        # print(f"start date {START_DATE}")
        # print(f"end date {END_DATE}")
        # breakpoint()
        print(f"\nProcessing team {team_name} (ID: {team_id})...")

        # --------------------- start of API request for events attended -----------------------------------
        base_url = f"https://www.robotevents.com/api/v2/teams/{team_id}/events"
        needed_parameters = { 
            "id[]" : f"{team_id}", 
            "start" : f"{START_DATE}",
            "end" : f"{END_DATE}",
        }

        my_headers = {
            "Authorization": f"Bearer {API_KEY}", 
            "Accept": "application/json"
        }


        # Get current file path to save .json file in the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"{team_name}_events.json"
        file_path = os.path.join(current_dir, filename)

        response = requests.get(base_url, params = needed_parameters, headers = my_headers)
        print("Status Code:", response.status_code)


        if response.status_code == 200:
            data = response.json()

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"Data saved to {file_path}.")

        else:
            print("Request for events attended failed.")

        # ---------------------------- end of API request for events attended --------------------------------

        # Get event IDs

        with open(file_path, "r") as f:
            data = json.load(f)

        # Extract event IDs
        event_ids = []

        for event in data.get("data", []):  # Use .get() to avoid crash if "data" missing
            event_id = event.get("id")
            if event_id is not None:
                event_ids.append(event_id)

        print(f"Found {len(event_ids)} event(s) in {file_path}:")
        print(event_ids)

        
        # Process team's performance in each event
        for event_id in event_ids:
            matches_won = 0

            print(f"\nProcessing {team_name} performance in event {event_id} ...")

            # --------------------- start of API request for team performance -----------------------------------
            base_url = f"https://www.robotevents.com/api/v2/teams/{team_id}/rankings"
            needed_parameters = { 
                "id[]" : f"{team_id}", 
                "event[]" : f"{event_id}",
            }

            my_headers = {
                "Authorization": f"Bearer {API_KEY}", 
                "Accept": "application/json"
            }


            # Get current file path to save .json file in the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            filename = f"{team_name}_{event_id}.json"
            file_path = os.path.join(current_dir, filename)

            response = requests.get(base_url, params = needed_parameters, headers = my_headers)
            print("Status Code:", response.status_code)


            if response.status_code == 200:
                data = response.json()

                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                
                print(f"Event data saved to {file_path}.")

            else:
                print("Request for team performance failed.")
                # print("Response text:", response.text)

            # ---------------------------- end of API request for team's performance --------------------------------


        # Analyze performance by event

        """
        num_matches = wins + losses + ties
        total_matches += num_matches
        awp = wp - 2 * wins - ties
        total_awp += awp
        """

        pattern = re.compile(rf"^{re.escape(team_name)}_(\d+)\.json$")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        time.sleep(0.005)
        
        # Loop through all matching files in the directory
        for filename in os.listdir(script_dir):
            # print(f"team_name: {team_name}")
            if pattern.match(filename):
                print(f"Processing {filename}...")
                file_path = os.path.join(script_dir, filename)
                with open(file_path, "r") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"  Skipping invalid JSON file: {filename}")
                        continue

                if not data.get("data"):
                    print(f"  Skipping empty data in {filename}")
                    continue
                # print("we start processing")
                for entry in data["data"]:
                    wins = entry.get("wins", 0)
                    losses = entry.get("losses", 0)
                    ties = entry.get("ties", 0)
                    wp = entry.get("wp", 0)

                    num_matches = wins + losses + ties
                    awp = wp - 2 * wins - ties

                    total_matches += num_matches
                    total_awp += awp
                    print(f"  Wins: {wins}, Losses: {losses} Ties: {ties}, WP: {wp}")
                    print(f"  awp: {awp}")
                    print(f"  total matches: {total_matches}, total awp: {total_awp}")

        # Output results
        print(f"Summary for team {team_name}:")
        print(f"Total Matches: {total_matches}")
        print(f"Total AWP: {total_awp}")

        if total_matches != 0:
            awp_ratio = total_awp / total_matches
        else:
            awp_ratio = 0
        print(f"awp_ratio: {awp_ratio}")
        
        # store [team number (or name as they call it), total_awp, total_matches, avg_awp]
        team_stats[team_name] = [total_awp, total_matches, awp_ratio]

print("final team_stats:")
print(team_stats)

# ====================================================================
# Step [] - Data visualization
# ====================================================================

sorted_teams = sorted(team_stats.items(), key=lambda x: x[1][2], reverse=True)
teams = [team for team, stats in sorted_teams]
avg_awps = [stats[2] for team, stats in sorted_teams]

fig = go.Figure(go.Bar(
    x=teams,
    y=avg_awps,
    marker_color='indigo'
))

fig.update_layout(
    title="Teams by Average AWP (Descending)",
    xaxis_title="Team",
    yaxis_title="Average AWP",
    xaxis_tickangle=-45,
    height=600
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pyo.plot(fig, filename="avg_awp.html", auto_open=True)

# helpful Bash command to remove .json files
# find . -maxdepth 1 -name "*.json" | grep -v -E "event.json|event_worlds.json" | xargs rm
