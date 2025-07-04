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
| `team.py` |gets information about a team, such as ID, Name, Organization, and Location|
