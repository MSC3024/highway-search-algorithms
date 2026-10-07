# Highway Search Algorithms

A Python graph-search project that compares **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Uniform-Cost Search (UCS)**, and **A\*** on a U.S. highway-routing network built from the team's collected Google Maps data.

## Project Motivation

The project applies four classic AI search algorithms to a practical route-finding problem. Cities are graph nodes and the collected city-to-city highway connections are weighted graph edges.

- **g(n):** accumulated driving distance in miles.
- **h(n):** straight-line distance estimate to the target in miles.
- **A\* evaluation:** `f(n) = g(n) + h(n)`.
- **Airplane-time estimate:** `h(n) / 250 mph`, following the assignment assumption.

## Dataset

The final dataset contains **11 cities and 17 highway connections** collected by the team using Google Maps.

Cities:

1. Saint Paul, Minnesota
2. Springfield, Illinois
3. Chicago, Illinois
4. Indianapolis, Indiana
5. Columbus, Ohio
6. Nashville, Tennessee
7. Atlanta, Georgia
8. Columbia, South Carolina
9. Washington, District of Columbia
10. Philadelphia, Pennsylvania
11. New York, New York

The authoritative collected data is stored in:

- `data/google_maps_collected.csv` - original normalized team data with road and plane distances.
- `data/roads.csv` - program-ready weighted-edge dataset.
- `data/cities.csv` - coordinates and state metadata used for mapping and heuristic fallback.

For a city pair that appears directly in the collected data, the program uses the team's collected straight-line value for `h(n)`. For other current-city/goal combinations needed by A\*, the program computes a direct great-circle estimate using the Haversine formula.

## Algorithms

| Algorithm | Edge weights | Heuristic | Search strategy |
|---|---:|---:|---|
| BFS | No | No | Explores level by level |
| DFS | No | No | Explores one branch deeply before backtracking |
| UCS | Yes | No | Expands the path with the smallest accumulated driving distance |
| A* | Yes | Yes | Expands the path with the smallest `g(n) + h(n)` |

## Project Structure

```text
highway-search-algorithms/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── cities.csv
│   ├── roads.csv
│   ├── google_maps_collected.csv
│   └── DATA_NOTES.md
├── src/
│   ├── __init__.py
│   ├── graph.py
│   ├── search.py
│   └── visualization.py
├── tests/
│   └── test_search.py
├── docs/
│   ├── REPORT_OUTLINE.md
│   ├── PRESENTATION_OUTLINE.md
│   └── FINAL_RESULTS.md
└── outputs/
    └── .gitkeep
```

## Setup

```bash
git clone https://github.com/Amereh11/highway-search-algorithms.git
cd highway-search-algorithms
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with:

```bash
.venv\Scripts\activate
```

## Run One Route

Example: Saint Paul to New York using all four algorithms.

```bash
python main.py --start "Saint Paul" --goal "New York" --algorithm all
```

Save route-map images as well:

```bash
python main.py --start "Saint Paul" --goal "New York" --algorithm all --save-maps
```

## Run Five Random Start/Target Pairs

```bash
python main.py --random 5 --seed 42
```

With route maps:

```bash
python main.py --random 5 --seed 42 --save-maps
```

## Verified Example: Saint Paul to New York

Using the team's final Google Maps road-distance dataset:

| Algorithm | Route distance | Nodes expanded |
|---|---:|---:|
| BFS | 1,287 mi | 11 |
| DFS | 1,287 mi | 5 |
| UCS | 1,287 mi | 10 |
| A* | 1,287 mi | 6 |

All four algorithms found the same route for this case:

`Saint Paul -> Chicago -> Columbus -> Philadelphia -> New York`

The direct straight-line estimate from Saint Paul to New York is approximately **1,007.6 miles**, which corresponds to about **4.03 hours** at 250 mph.

## Five Seeded Random Tests

With `--random 5 --seed 42`, the program evaluates these start/goal pairs:

1. Washington -> Chicago
2. Atlanta -> Indianapolis
3. Columbus -> Washington
4. Columbia -> Chicago
5. Washington -> Saint Paul

Across these tests, UCS and A* return the same minimum-cost route distances, while A* generally expands fewer nodes because the heuristic guides the search toward the target.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

The test suite checks:

- all four algorithms can find a route,
- the final dataset contains 11 cities and 17 edges,
- UCS and A* agree on the optimal route cost for the main test,
- collected straight-line data is used for direct pairs,
- `h(goal) = 0`, and
- the 250 mph flight-time calculation is correct.

## Assignment Coverage

This repository implements the programming requirements of the project:

- 10-15 cities: **11 included**
- highway connections across multiple states/regions
- Google Maps driving distances for `g(n)`
- straight-line estimates for `h(n)`
- BFS
- DFS
- UCS
- A*
- user-selected start and target cities
- five random start/target cases
- route and distance output
- map visualization
- automated tests

## Team

The project was completed collaboratively by **Motasem Amereh, Tammanna, Manjot, Thomas, and Parv**. Responsibilities were divided across data preparation, algorithm implementation, integration, testing, visualization, analysis, and documentation, with all contributions presented as equal parts of the final project.
