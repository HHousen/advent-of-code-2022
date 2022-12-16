import re
from functools import cache
import networkx as nx

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

valves = set()
flow_rates = {}
edges = set()

for valve, flow_rate, destinations in re.findall(
    r"Valve (\w+) .*=(\d+); .* valves? (.*)", puzzle_input
):
    valves.add(valve)
    if flow_rate != "0":
        flow_rates[valve] = int(flow_rate)
    for destination in destinations.split(","):
        edges.add((valve, destination.strip()))

graph = nx.DiGraph()
graph.add_edges_from(edges)
# Compute the shortest path length between all valves. `distances` is a
# dictionary of the form {valve_1: {valve_1: 0, valve_2: 1, valve_3: 4, ...},
# valve_2: {valve_1: 1, ...}, ...} where the values are the distances between
# the valves. So, distances[valve_1][valve_2] is the distance from valve_1 to
# valve_2. Distance here means time to travel to that node.
distances = dict(nx.all_pairs_shortest_path_length(graph))


# Simple memoization provided by functools
@cache
def search(
    time,
    start_valve="AA",
    unopened_valves=frozenset(flow_rates),
    elephant_available=False,
):
    # The i-th index in `pressure_released` contains the maximum pressure
    # released by choosing to open the i-th valve next (after `start_valve`).
    pressure_released = []
    # For each unopened valve v...
    for valve in unopened_valves:
        # Check if we can traverse to valve v in the remaining time. If the
        # valve can be opened in time...
        if distances[start_valve][valve] < time:
            # Compute the new time remaining after opening valve v.
            new_time_remaining = time - distances[start_valve][valve] - 1
            # The pressure released from opening valve v is the time v will be
            # open (`new_time_remaining`) times the flow rate for v PLUS any
            # additional pressure released from valves we open after v. So, we
            # recursively call `search`. The new call to search will explore
            # all options for valves to open after v and will select the valve
            # that results in the most pressure released. The new call to
            # `search` receives the list of unopened valves excluding the one
            # we just opened.
            pressure_released.append(
                flow_rates[valve] * new_time_remaining
                + search(
                    new_time_remaining,
                    valve,
                    unopened_valves - {valve},
                    elephant_available,
                )
            )
    # If we are solving part 2 and can use the elephant, then find the optimal
    # path (releases the most pressure) for the elephant such that the path
    # does not overlap with any valves opened by the human. For instance, if we
    # are a few levels deep in recursive calls, then we have constructed a path
    # of valves to open. For this partial path, calculate the optimal path for
    # the elephant starting from AA excluding the valves we've opened on our
    # path thus far. So, after many recursive calls, the values in
    # `pressure_released` for the human's possible options will be smaller than
    # the final value in `pressure_released` (the pressure released by the
    # elephant) as the human runs out of time. At this point, the elephant's
    # path will be explore as an alternative. One example where this can help
    # is if there is a somewhat valuable valve close to AA that the elephant
    # could open sooner (thus releasing more pressure proportional to the time
    # it is open) than the human could along its optimal path.
    # TL;DR: For each possible path of valves the human can take, check how
    # much pressure the elephant could release.
    if elephant_available:
        pressure_released += [search(26, unopened_valves=unopened_valves)]
    # If we were able to release additional pressure, return the maximum
    # pressure released out of all paths explored.
    if pressure_released:
        return max(pressure_released)
    # If no more pressure could be released, return 0.
    return 0


part1_solution = search(30)

# Part 1 Solution: 2056
print(f"Part 1 Solution: {part1_solution}")

# In part 2, we have access to the elephant.
part2_solution = search(26, elephant_available=True)

# Part 2 Solution: 2513
print(f"Part 2 Solution: {part2_solution}")
