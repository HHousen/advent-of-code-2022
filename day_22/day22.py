import re

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

grid_txt, path_txt = puzzle_input.split("\n\n")
grid_txt = grid_txt.splitlines()

grid = {
    (x, y): value
    for y, row in enumerate(grid_txt)
    for x, value in enumerate(row)
    if value in ".#"
}
# Find all numbers (up to two digits) or an "R" or an "L"
path = re.findall("\d+|[RL]", path_txt)
# Convert all the movement amount numbers to actual integers. Leave the Rs and
# Ls alone.
path = [int(x) if x.isnumeric() else x for x in path]

# Map the direction the player is facing to the corresponding value for the
# final answer.
facing_val = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}


def part1_wrap(position, facing):
    # Move backwards to find wrap around location
    search_position = position
    # Keep searching in the opposite direction the player is facing until the
    # `search_position` is no longer in the grid.
    while search_position in grid:
        new_position = search_position
        search_position = (
            search_position[0] - facing[0],
            search_position[1] - facing[1],
        )
    # Return the position just before the search position moved out of the grid.
    return new_position, facing


def part2_wrap(position, facing):
    x, y = position
    # Divide by 50 because the sides of the cube are 50x50.
    # ASCII art visualization of the cube. This shows where the player will
    # wrap around in 2d space based on a 3d folding of the cube.
    #        ••••••••••       ••••••
    #      ••          ••     •     ••
    #     ••           █████████      •
    #     •       •••••█   █   █••     •
    #    ••    ••••    █   █   █ ••    •
    #    •    ••       █████████  •    •
    #    •   ••      ••█   █ •    •    •
    #    •   •       • █   █••    •    •
    #    ••   •    █████████     ••   ••
    #     •   •••••█   █   █••••••   ••
    #     •        █   █   █         •
    #      ••      █████████       •••
    #       ••••   █   █ •        ••
    #          ••••█   █••      •••
    #              █████       ••
    #                 •      ••
    #                 •••••••
    match facing, y // 50, x // 50:
        case (1, 0), 0, _: return (99, 149 - y), (-1, 0)
        case (1, 0), 1, _: return (y + 50, 49), (0, -1)
        case (1, 0), 2, _: return (149, 149 - y), (-1, 0)
        case (1, 0), 3, _: return (y - 100, 149), (0, -1)
        case (-1, 0), 0, _: return (0, 149 - y), (1, 0)
        case (-1, 0), 1, _: return (y - 50, 100), (0, 1)
        case (-1, 0), 2, _: return (50, 149 - y), (1, 0)
        case (-1, 0), 3, _: return (y - 100, 0), (0, 1)
        case (0, 1), _, 0: return (x + 100, 0), (0, 1)
        case (0, 1), _, 1: return (49, 100 + x), (-1, 0)
        case (0, 1), _, 2: return (99, -50 + x), (-1, 0)
        case (0, -1), _, 0: return (50, 50 + x), (1, 0)
        case (0, -1), _, 1: return (0, 100 + x), (1, 0)
        case (0, -1), _, 2: return (x - 100, 199), (0, -1)


def solve(part2=False):
    # The player starts in the top left.
    position = (grid_txt[0].index("."), 0)
    # Initial direction play is facing.
    facing = (1, 0)
    for move in path:
        if move == "R":
            facing = (-facing[1], facing[0])
        elif move == "L":
            facing = (facing[1], -facing[0])
        else:
            for _ in range(move):
                # Move one in the direction the player is facing.
                new_position = (position[0] + facing[0], position[1] + facing[1])
                new_facing = facing
                # If this new location is not in the grid, wrap around using
                # the algorithm appropriate for each part of the challenge.
                if new_position not in grid:
                    new_position, new_facing = (
                        part2_wrap(position, facing)
                        if part2
                        else part1_wrap(position, facing)
                    )
                cell = grid[new_position]
                if cell == ".":
                    # Update the position and direction facing if not a wall.
                    position = new_position
                    facing = new_facing
                if cell == "#":
                    # Stop moving if we hit and wall. Go to the next move.
                    break

    # Calculate the "password."
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + facing_val[facing]


part1_solution = solve()

# Part 1 Solution: 196134
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solve(part2=True)

# Part 2 Solution: 146011
print(f"Part 2 Solution: {part2_solution}")
