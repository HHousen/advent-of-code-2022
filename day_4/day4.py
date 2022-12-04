with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

part1_solution = 0
part2_solution = 0
for pair in puzzle_input.split("\n"):
    assignment1, assignment2 = pair.split(",")
    a1, a2 = [int(x) for x in assignment1.split("-")]
    b1, b2 = [int(x) for x in assignment2.split("-")]
    if (a1 <= b1 and a2 >= b2) or (b1 <= a1 and b2 >= a2):
        part1_solution += 1
    if (not a2 < b1) and (not b2 < a1):
        part2_solution += 1


# Part 1 Solution: 573
print(f"Part 1 Solution: {part1_solution}")

# Part 2 Solution: 867
print(f"Part 2 Solution: {part2_solution}")
