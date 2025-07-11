
### The Algorithm
1. start with the current event - get event id (using event script)
2. use event id to get list of teams participating in that event (a teams script)
3. get information about our team in this event (event script with event id specified)
4. for all teams in that event in the same division, tally up their autonomous win points
   1. all the events they've participated in (use events script) - check that they have registered
   2. to this day (specify date range)
   3. for each event, find number of Qualification Matches - this dictates the max # of aps possible
   4. calculate the % success rate based on the team's total ap / max ap
   5. save team & their success rate  to .xlsx?
6. arrange teams from highest ap to lowest ap
7. output [Team, ap] in descending order
8. data visualization - interactive graphs? 

### `config_interactive.py` Template
API_KEY = ""
TEAM_NUMBER = ""
EVENT_SKU = "RE-VURC-xx-yyyy"
START_DATE = "2024-05-13"
END_DATE = "2025-05-03"
SEASON = 191 # 2024-2025 High Stakes VURC
