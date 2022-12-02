with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

instructions = puzzle_input.split("\n")


mapping = {"A": "X", "B": "Y", "C": "Z"}
points = 0
for instruction in instructions:
    one, two = instruction.split(" ")
    points += ord(two) - ord("W")
    if (
        (one == "A" and two == "Y")
        or (one == "B" and two == "Z")
        or (one == "C" and two == "X")
    ):
        points += 6
    elif mapping[one] == two:
        points += 3


part1_solution = points

# Part 1 Solution: 15337
print(f"Part 1 Solution: {part1_solution}")

winner = {"A": "B", "B": "C", "C": "A"}
loser = {"A": "C", "B": "A", "C": "B"}
points = 0
for instruction in instructions:
    one, two = instruction.split(" ")
    if two == "X":
        shape = loser[one]
    elif two == "Y":
        shape = one
        points += 3
    elif two == "Z":
        shape = winner[one]
        points += 6
    points += ord(shape) - ord("@")

part2_solution = points

# Part 2 Solution: 11696
print(f"Part 2 Solution: {part2_solution}")
