### VEX API
https://www.robotevents.com/api/v2


### Instructions
1. log in
2. create Access Token to become authorized
3. paste your Access Token into config.py to be used in code files to get response

<br>

> [!Note]
> It is way easier to work with APIs using Python in this case where millisecond performance doesn't matter.
>
> In Python, you just press "run" and get your reponse.
>
> In C++, there are several libraries and workloads you need to download. Plus, you need to repeat the entire build process every time you make a change.
> I have included an example of making API requests using C++ in the `cmake` folder, with instructions.
> 


### Files and their functions
| File | Purpose |
|------|---------|
| [event_matches.py](./Python/event_matches.py) | produces a .json file containing all matches at an event.|
| [event.py](./Python/event.py) | gets information such as date, location, divisions, programs, and IDabout one event using its SKU. |
| [events_attended.py](./Python/events_attended.py) | obtains a list of events a team has attended in the specified time frame |
| [programs.py](./Python/programs.py) | lists all programs offered by VEX. Specifically, V5RC, VURC, WORKSHOP, VGOC, FAC, and VAIRC. |
| [rankings_in_division.py](./Python/rankings_in_division.py) | obtains the rankings of all teams in one division. |
| [team.py](./Python/team.py) | gets information about a team, including team ID, number, name, organization, and location. |
| [teams_all.py](./Python/teams_all.py) | gets all teams participating in VEX. |
| [teams_at_event.py](./Python/teams_at_event.py) | obtains a list of all teams attending a particular event. |
| [event_worlds.py](./Python/25-Worlds-Dallas/event_worlds.py) | information on Worlds in May 2025. | 


#### Closing Tasks
- rename variables for clarity in `avg_awp.py` 
- add sample output png to `README.md`
