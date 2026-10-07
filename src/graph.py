from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


EARTH_RADIUS_MILES = 3958.8
AIRPLANE_SPEED_MPH = 250.0


@dataclass(frozen=True)
class City:
    name: str
    latitude: float
    longitude: float


class HighwayGraph:
    def __init__(self) -> None:
        self.cities: dict[str, City] = {}
        self.adjacency: dict[str, list[tuple[str, float]]] = {}
        self.plane_distances: dict[tuple[str, str], float] = {}

    @classmethod
    def from_csv(cls, cities_path: Path, roads_path: Path) -> "HighwayGraph":
        graph = cls()

        with cities_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                graph.add_city(
                    row["city"],
                    float(row["latitude"]),
                    float(row["longitude"]),
                )

        with roads_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                plane_raw = row.get("plane_miles", "")
                plane_miles = float(plane_raw) if plane_raw not in ("", None) else None
                graph.add_road(
                    row["city_a"],
                    row["city_b"],
                    float(row["driving_miles"]),
                    plane_miles,
                )

        return graph

    def add_city(self, name: str, latitude: float, longitude: float) -> None:
        self.cities[name] = City(name, latitude, longitude)
        self.adjacency.setdefault(name, [])

    def add_road(
        self,
        city_a: str,
        city_b: str,
        driving_miles: float,
        plane_miles: float | None = None,
    ) -> None:
        self.validate_city(city_a)
        self.validate_city(city_b)

        self.adjacency[city_a].append((city_b, driving_miles))
        self.adjacency[city_b].append((city_a, driving_miles))

        if plane_miles is not None:
            self.plane_distances[(city_a, city_b)] = plane_miles
            self.plane_distances[(city_b, city_a)] = plane_miles

        self.adjacency[city_a].sort(key=lambda item: item[0])
        self.adjacency[city_b].sort(key=lambda item: item[0])

    def validate_city(self, name: str) -> None:
        if name not in self.cities:
            available = ", ".join(sorted(self.cities))
            raise ValueError(f"Unknown city '{name}'. Available cities: {available}")

    def city_names(self) -> list[str]:
        return sorted(self.cities)

    def neighbors(self, city: str) -> list[tuple[str, float]]:
        self.validate_city(city)
        return list(self.adjacency[city])

    def edge_distance(self, city_a: str, city_b: str) -> float:
        for neighbor, distance in self.adjacency[city_a]:
            if neighbor == city_b:
                return distance
        raise ValueError(f"No direct road between {city_a} and {city_b}")

    def collected_plane_distance(self, city_a: str, city_b: str) -> float | None:
        """Return the team's collected Google Maps straight-line value for a direct pair."""
        self.validate_city(city_a)
        self.validate_city(city_b)
        return self.plane_distances.get((city_a, city_b))

    def path_distance(self, path: list[str]) -> float:
        if len(path) < 2:
            return 0.0
        return sum(
            self.edge_distance(path[i], path[i + 1])
            for i in range(len(path) - 1)
        )

    def heuristic_miles(self, city_a: str, city_b: str) -> float:
        """
        Straight-line estimate h(n).

        If the team collected this exact city pair in Google Maps, use that
        measured value. Otherwise compute the direct great-circle distance
        from the city coordinates with the Haversine formula. This lets A*
        evaluate any current-city/goal pair while preserving collected values
        whenever they are available.
        """
        self.validate_city(city_a)
        self.validate_city(city_b)

        collected = self.collected_plane_distance(city_a, city_b)
        if collected is not None:
            return collected

        a = self.cities[city_a]
        b = self.cities[city_b]

        lat1 = math.radians(a.latitude)
        lon1 = math.radians(a.longitude)
        lat2 = math.radians(b.latitude)
        lon2 = math.radians(b.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        hav = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        central_angle = 2 * math.asin(math.sqrt(hav))
        return EARTH_RADIUS_MILES * central_angle

    def estimated_flight_time_hours(self, city_a: str, city_b: str) -> float:
        return self.heuristic_miles(city_a, city_b) / AIRPLANE_SPEED_MPH
