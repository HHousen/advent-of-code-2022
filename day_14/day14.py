from copy import deepcopy


with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

paths = [
    [list(map(int, coords.split(","))) for coords in path.split(" -> ")]
    for path in puzzle_input.split("\n")
]

filled = set()
abyss_y = 0
for path in paths:
    for (x, y), (a, b) in zip(path, path[1:]):
        x, a = min(x, a), max(x, a)
        y, b = min(y, b), max(y, b)
        if x - a == 0:  # moving in y direction
            filled |= {(x, z) for z in range(y, b + 1)}
        elif y - b == 0:  # moving in x direction
            filled |= {(z, y) for z in range(x, a + 1)}
            abyss_y = max(abyss_y, b + 1)


def solution(filled, part2=False):
    sand_start = (500, 0)
    sand_x, sand_y = sand_start
    num_sand_at_rest = 0
    while True:
        if part2:
            if sand_start in filled:
                # Part 2 ending condition
                break
        elif sand_y >= abyss_y:
            # Part 1 ending condition
            break
        # Check each possible sand position. If not filled then move the sand
        # to its new spot and go to the next iteration.
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            new_sand_x, new_sand_y = sand_x + dx, sand_y + dy
            # `and not (sand_y >= abyss_y)` is included for part 2. In part 2,
            # the floor is directly below abyss_y. So, y positions greater than
            # `abyss_y` are invalid, but `new_sand_y==abyss_y` is valid.
            if (new_sand_x, new_sand_y) not in filled and not (new_sand_y > abyss_y):
                sand_x, sand_y = new_sand_x, new_sand_y
                break
        else:
            # If loop doesn't break (aka we don't find a new spot for the sand to
            # go), the sand is at rest. So, add the sand as an occupied location.
            filled.add((sand_x, sand_y))
            num_sand_at_rest += 1
            sand_x, sand_y = sand_start
    return num_sand_at_rest


part1_solution = solution(deepcopy(filled))

# Part 1 Solution: 862
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solution(filled, part2=True)

# Part 2 Solution: 28744
print(f"Part 2 Solution: {part2_solution}")
