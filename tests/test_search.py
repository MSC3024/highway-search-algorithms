import unittest
from pathlib import Path

from src.graph import HighwayGraph
from src.search import bfs, dfs, ucs, astar


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class SearchAlgorithmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = HighwayGraph.from_csv(
            PROJECT_ROOT / "data" / "cities.csv",
            PROJECT_ROOT / "data" / "roads.csv",
        )

    def test_dataset_shape(self):
        self.assertEqual(len(self.graph.city_names()), 11)
        undirected_edges = sum(len(v) for v in self.graph.adjacency.values()) // 2
        self.assertEqual(undirected_edges, 17)

    def test_all_algorithms_find_route(self):
        start = "Saint Paul"
        goal = "New York"

        for search in (bfs, dfs, ucs, astar):
            result = search(self.graph, start, goal)
            self.assertIsNotNone(result.path)
            self.assertEqual(result.path[0], start)
            self.assertEqual(result.path[-1], goal)
            self.assertGreater(result.distance, 0)

    def test_ucs_and_astar_have_same_optimal_cost(self):
        start = "Saint Paul"
        goal = "New York"

        ucs_result = ucs(self.graph, start, goal)
        astar_result = astar(self.graph, start, goal)

        self.assertAlmostEqual(ucs_result.distance, astar_result.distance)

    def test_collected_heuristic_is_used_for_direct_pair(self):
        self.assertAlmostEqual(
            self.graph.heuristic_miles("Saint Paul", "Chicago"),
            346.44,
            places=2,
        )

    def test_heuristic_is_zero_at_goal(self):
        city = "Atlanta"
        self.assertAlmostEqual(self.graph.heuristic_miles(city, city), 0.0)

    def test_flight_time_formula(self):
        h = self.graph.heuristic_miles("Saint Paul", "Chicago")
        t = self.graph.estimated_flight_time_hours("Saint Paul", "Chicago")
        self.assertAlmostEqual(t, h / 250.0)


if __name__ == "__main__":
    unittest.main()
