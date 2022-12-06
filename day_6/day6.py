with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()


def solve(num_distinct=4):
    for idx in range(num_distinct, len(puzzle_input)):
        previous_chars = puzzle_input[idx - num_distinct : idx]
        if len(set(previous_chars)) == num_distinct:
            break
    return idx


part1_solution = solve(4)

# Part 1 Solution: 1343
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solve(14)

# Part 2 Solution: 2193
print(f"Part 2 Solution: {part2_solution}")
