from collections import defaultdict


with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip().splitlines()

all_neighbors = [
    (0, -1),
    (-1, -1),
    (1, -1),
    (0, 1),
    (-1, 1),
    (1, 1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, 0),
    (1, -1),
    (1, 1),
]

grid = {
    (x, y)
    for y, row in enumerate(puzzle_input)
    for x, value in enumerate(row)
    if value == "#"
}

proposals = [
    lambda coords: [
        (coords[0] + offset[0], coords[1] + offset[1])
        for offset in [(0, -1), (-1, -1), (1, -1)]
    ],
    lambda coords: [
        (coords[0] + offset[0], coords[1] + offset[1])
        for offset in [(0, 1), (-1, 1), (1, 1)]
    ],
    lambda coords: [
        (coords[0] + offset[0], coords[1] + offset[1])
        for offset in [(-1, 0), (-1, -1), (-1, 1)]
    ],
    lambda coords: [
        (coords[0] + offset[0], coords[1] + offset[1])
        for offset in [(1, 0), (1, -1), (1, 1)]
    ],
]

num_moved = -1
step = 0
# If no elves have moved then we have the answer to part 2. Keep stepping until
# no elves have moved.
while num_moved:
    if step == 10:  # Part 1 solution found
        max_x = max(x for x, _ in grid)
        max_y = max(y for _, y in grid)
        min_x = min(x for x, _ in grid)
        min_y = min(y for _, y in grid)
        # Calculate the total area of the the region with elves and subtract
        # the number of elves in that region to find the empty spaces.
        part1_solution = (max_x - min_x + 1) * (max_y - min_y + 1) - len(grid)

        # Part 1 Solution: 4025
        print(f"Part 1 Solution: {part1_solution}")

    proposed_moves = defaultdict(list)
    for coords in grid:
        # If the elf has no elves surrounding it, then it does not move.
        if all(
            (coords[0] + offset[0], coords[1] + offset[1]) not in grid
            for offset in all_neighbors
        ):
            continue
        # Check each direction the elf can move and see if it meets the
        # criteria.
        for proposal in proposals:
            # `prop` is a list of the coordinates to check for elves
            prop = proposal(coords)
            # If all necessary coordinates are empty, then the elf at position
            # `coords` wants to move to `prop[0]`.
            if all(x not in grid for x in prop):
                proposed_moves[prop[0]].append(coords)
                break

    num_moved = 0
    for destination, start_locations in proposed_moves.items():
        # Only one elf can move to each new coordinate. So, only perform the
        # move if the number of elves wanting to move to that position is 0.
        if len(start_locations) == 1:
            # Remove the elf from its current position...
            grid.remove(start_locations[0])
            # ...and add it to its new position.
            grid.add(destination)
            num_moved += 1
    step += 1

    # Move the first move proposal function to the end of the list so it is
    # checked last.
    proposals.append(proposals.pop(0))

part2_solution = step

# Part 2 Solution: 935
print(f"Part 2 Solution: {part2_solution}")
