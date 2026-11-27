import heapq
import json
import unittest
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).with_name("Portmantout-optimal.ipynb")


def load_solver():
    notebook = json.loads(NOTEBOOK_PATH.read_text())
    source_by_role = {}

    # Load definitions only; the notebook's full-wordlist cell is deliberately skipped.
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        if "from scipy.optimize import" in source:
            source_by_role["imports"] = source
        elif "class OverlapGraph:" in source:
            source_by_role["graph"] = source
        elif "def solve_optimal_portmantout(" in source:
            source_by_role["solver"] = source

    required_roles = ("imports", "graph", "solver")
    missing_roles = [role for role in required_roles if role not in source_by_role]
    if missing_roles:
        raise RuntimeError(f"Could not locate notebook definition cells: {missing_roles}")

    namespace = {}
    for role in required_roles:
        exec(compile(source_by_role[role], f"{NOTEBOOK_PATH} ({role})", "exec"), namespace)
    return namespace


SOLVER = load_solver()
solve_optimal_portmantout = SOLVER["solve_optimal_portmantout"]
is_portman = SOLVER["is_portman"]


def required_words(words):
    return {
        word
        for word in words
        if not any(word != other and word in other for other in words)
    }


def brute_minimum_length(words):
    """Find the exact length with Dijkstra over (covered words, last word)."""
    required = required_words(words)
    required_bit = {word: 1 << i for i, word in enumerate(sorted(required))}
    full_mask = (1 << len(required)) - 1
    distances = {}
    queue = []

    for word in words:
        state = (required_bit.get(word, 0), word)
        cost = len(word)
        if cost < distances.get(state, float("inf")):
            distances[state] = cost
            heapq.heappush(queue, (cost, *state))

    while queue:
        cost, mask, previous = heapq.heappop(queue)
        if cost != distances[(mask, previous)]:
            continue
        if mask == full_mask:
            return cost

        for word in words:
            overlap = max(
                (
                    size
                    for size in range(1, min(len(previous), len(word)))
                    if previous[-size:] == word[:size]
                ),
                default=0,
            )
            if not overlap:
                continue

            next_state = (mask | required_bit.get(word, 0), word)
            next_cost = cost + len(word) - overlap
            if next_cost < distances.get(next_state, float("inf")):
                distances[next_state] = next_cost
                heapq.heappush(queue, (next_cost, *next_state))

    return None


class PortmantoutConnectivityTests(unittest.TestCase):
    def assert_optimal_portmantout(self, words, expected_components):
        result = solve_optimal_portmantout(words)
        self.assertEqual(result.lp_components, expected_components)
        self.assertEqual(result.length, brute_minimum_length(words))
        self.assertEqual(len(result.string), result.length)
        self.assertLessEqual(result.lp_lower_bound, result.length)
        self.assertTrue(is_portman(result.path, words, required_words(words)))
        return result

    def test_connected_lp_solution(self):
        words = {"acac", "acbb", "bbbc", "cab", "caba", "cabb", "cacc"}

        result = self.assert_optimal_portmantout(words, expected_components=1)

        self.assertFalse(result.reconnected_zero_cost)
        self.assertEqual(result.milp_cuts_added, 0)

    def test_zero_cost_reconnection(self):
        words = {"baac", "bbaa", "bbbc", "ca", "caab", "cbbc", "cbc"}

        result = self.assert_optimal_portmantout(words, expected_components=2)

        self.assertTrue(result.reconnected_zero_cost)
        self.assertEqual(result.milp_cuts_added, 0)

    def test_milp_connectivity_fallback(self):
        words = {"aaac", "cbc", "cc"}

        result = self.assert_optimal_portmantout(words, expected_components=2)

        self.assertFalse(result.reconnected_zero_cost)
        self.assertGreater(result.milp_cuts_added, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
