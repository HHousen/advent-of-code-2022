from collections import deque

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

cubes = {tuple(map(int, coords.split(","))) for coords in puzzle_input.split("\n")}


def neighbors(x, y, z):
    return {
        (x, y, z - 1),
        (x, y, z + 1),
        (x, y - 1, z),
        (x, y + 1, z),
        (x - 1, y, z),
        (x + 1, y, z),
    }


# For each lava cube, count how many neighbors are not lava cubes (and thus are
# air cubes).
part1_solution = sum(
    neighbor not in cubes for cube in cubes for neighbor in neighbors(*cube)
)

# Part 1 Solution: 4308
print(f"Part 1 Solution: {part1_solution}")

# Create a bounding box around the lava droplet.
min_x = min(x for x, _, _ in cubes) - 1
max_x = max(x for x, _, _ in cubes) + 1
min_y = min(y for _, y, _ in cubes) - 1
max_y = max(y for _, y, _ in cubes) + 1
min_z = min(z for _, _, z in cubes) - 1
max_z = max(z for _, _, z in cubes) + 1

queue = deque()
# Start searching from the corner of the bounding box with smallest
# coordinates.
queue.append((min_x, min_y, min_z))
# Keep track of the positions visited, which are the cubes of air outside
# of the lava droplet.
outside_air = set()
while queue:
    x, y, z = cube = queue.popleft()
    # We only want to explore air cubes near the lava droplet, otherwise we
    # would add points further and further away from the droplet to the
    # queue.
    if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
        for neighbor in neighbors(*cube):
            # If the neighbor hasn't already been visited and is not part
            # of the lava droplet, then it is an air cube and its neighbors
            # should be visited.
            if neighbor not in cubes and neighbor not in outside_air:
                # Add the neighbor to the queue so its neighbors are
                # visited.
                queue.append(neighbor)
                # Keep track of the cubes that are air within our bounding
                # box.
                outside_air.add(neighbor)

# For each lava cube, count how many neighbors are part of the air outside of
# the lava droplet.
part2_solution = sum(
    neighbor in outside_air for cube in cubes for neighbor in neighbors(*cube)
)

# Part 2 Solution: 2540
print(f"Part 2 Solution: {part2_solution}")
