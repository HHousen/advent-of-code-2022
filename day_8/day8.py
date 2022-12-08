import numpy as np

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

grid = np.array([[int(x) for x in line.strip()] for line in puzzle_input.split("\n")])
part1_grid = np.zeros_like(grid, int)
part2_grid = np.ones_like(grid, int)

for y, x in np.ndindex(grid.shape):
    current_value = grid[y, x]
    all_directions = [
        grid[y, x + 1 :],
        grid[y, :x][::-1],
        grid[y + 1 :, x],
        grid[:y, x][::-1],
    ]
    for direction in all_directions:
        lower = [val < current_value for val in direction]
        already_visible = part1_grid[y, x]
        all_lower = all(lower)

        part1_grid[y, x] = already_visible if already_visible else all_lower
        part2_grid[y, x] *= len(lower) if all_lower else lower.index(False) + 1


part1_solution = part1_grid.sum()

# Part 1 Solution: 1736
print(f"Part 1 Solution: {part1_solution}")

part2_solution = part2_grid.max()

# Part 2 Solution: 268800
print(f"Part 2 Solution: {part2_solution}")
