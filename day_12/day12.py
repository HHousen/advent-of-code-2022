import numpy as np
import networkx as nx

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

grid = np.array([list(line) for line in puzzle_input.split("\n")])
# "Your current position (S) has elevation a, and the location that should get
# the best signal (E) has elevation z."
start_coords = np.where(grid == "S")
start_coords = (start_coords[0][0], start_coords[1][0])
end_coords = np.where(grid == "E")
end_coords = (end_coords[0][0], end_coords[1][0])
grid[start_coords] = "a"
grid[end_coords] = "z"
grid = np.vectorize(ord)(grid)

graph = nx.grid_2d_graph(len(grid), len(grid[0]), create_using=nx.DiGraph)
graph.remove_edges_from(
    [
        (node_a, node_b)
        for node_a, node_b in graph.edges
        if grid[node_b] > grid[node_a] + 1
    ]
)

shortest_path_lengths = nx.shortest_path_length(graph, target=end_coords)

part1_solution = shortest_path_lengths[start_coords]

# Part 1 Solution: 484
print(f"Part 1 Solution: {part1_solution}")

part2_solution = min(
    shortest_path_lengths[coords]
    for coords in shortest_path_lengths
    if grid[coords] == ord("a")
)

# Part 2 Solution: 478
print(f"Part 2 Solution: {part2_solution}")
