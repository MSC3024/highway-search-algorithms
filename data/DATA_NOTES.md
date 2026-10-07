# Data Notes

The final highway graph is based on the team's collected Google Maps spreadsheet.

- `google_maps_collected.csv` preserves the collected city pairs, road distances, and straight-line distances.
- `roads.csv` is the program-ready version of the same 17 connections.
- `cities.csv` adds city coordinates and state metadata for visualization and for A* heuristic calculations when the current city and goal are not one of the directly measured pairs.

## Heuristic handling

For directly collected city pairs, the program uses the team's `h(n)` value exactly.

A* may also need `h(n)` between a current city and a target that are not directly connected by a road edge. For those pairs, the program uses the Haversine great-circle distance between the city coordinates. This keeps `h(n)` in miles and makes it compatible with the driving-distance cost `g(n)`.

The assumed airplane speed is 250 miles per hour, so estimated direct-flight time is:

`time = h(n) / 250`
