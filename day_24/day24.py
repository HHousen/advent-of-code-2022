import itertools

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip().splitlines()

directions = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

# Create a set of all the blizzards starting locations and their directions.
blizzards = {
    (x - 1, y - 1, directions[value])
    for y, row in enumerate(puzzle_input)
    for x, value in enumerate(row)
    if value not in ".#"
}

# Get the upper x and y bounds of the grid.
X = max(x for x, _, _ in blizzards) + 1
Y = max(y for _, y, _ in blizzards) + 1

# Define the starting and exit locations.
start = (0, -1)
exit = (X - 1, Y)


def solve(start, destinations, starting_step):
    # `visited` keeps track of all coordinates that can be visited by the
    # current `step`.
    visited = {start}
    # Keep stepping until we have visited all of the destination.
    for step in itertools.count(starting_step):
        # Determine the current blizzard locations. Move the blizzards in their
        # direction and wrap around if necessary.
        blizzard_locations = {
            ((x + step * dx) % X, (y + step * dy) % Y) for x, y, (dx, dy) in blizzards
        }
        # Create a set of the new moves we can make from every coordinate we've
        # visited so far. If a blizzard moves into a space we occupied before,
        # it will be removed from the list of new moves since we cannot wait in
        # that spot anymore.
        new_moves = {
            (x + dx, y + dy)
            for dx, dy in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
            for x, y in visited
            # Only consider the new location if it is inside the bounds of the
            # grid or if it is one of the destinations.
            if (0 <= x + dx < X and 0 <= y + dy < Y) or (x + dx, y + dy) in destinations
        }
        # The locations visited are the new moves that are not the locations of
        # blizzards.
        visited = new_moves - blizzard_locations
        # If we have reached the first destination...
        if destinations[0] in visited:
            # ...and this is the only destination left, then return the number
            # of steps to reach this destination.
            if len(destinations) <= 1:
                return step
            # If there are more destinations remaining, reset the set of
            # visited coordinates to the destination we just got to and start
            # trying to get to the second destination in the list.
            visited = {destinations.pop(0)}


part1_solution = solve(start, [exit], starting_step=1)

# Part 1 Solution: 299
print(f"Part 1 Solution: {part1_solution}")

# For part 2, we are starting at the exit from part 1 and trying to get back to
# the start and then to the exit again.
destinations = [start, exit]
part2_solution = solve(exit, destinations, starting_step=part1_solution)

# Part 2 Solution: 899
print(f"Part 2 Solution: {part2_solution}")
