# Final Experimental Results

Dataset: 11 cities, 17 team-collected Google Maps road connections.

## Main route: Saint Paul -> New York

All four algorithms return:

`Saint Paul -> Chicago -> Columbus -> Philadelphia -> New York`

Total driving distance: **1,287 miles**.

| Algorithm | Nodes expanded |
|---|---:|
| BFS | 11 |
| DFS | 5 |
| UCS | 10 |
| A* | 6 |

Direct heuristic from Saint Paul to New York: approximately **1,007.6 miles**.
Estimated direct-flight time at 250 mph: approximately **4.03 hours**.

## Five seeded random tests (`--seed 42`)

| Start | Goal | BFS | DFS | UCS | A* |
|---|---|---:|---:|---:|---:|
| Washington | Chicago | 723 | 1,411 | 723 | 723 |
| Atlanta | Indianapolis | 536 | 1,264 | 536 | 536 |
| Columbus | Washington | 398 | 398 | 398 | 398 |
| Columbia | Chicago | 933 | 933 | 933 | 933 |
| Washington | Saint Paul | 1,121 | 1,809 | 1,121 | 1,121 |

Average route distances:

- BFS: **742.2 miles**
- DFS: **1,163.0 miles**
- UCS: **742.2 miles**
- A*: **742.2 miles**

Average nodes expanded:

- BFS: **7.4**
- DFS: **7.4**
- UCS: **7.6**
- A*: **3.8**
