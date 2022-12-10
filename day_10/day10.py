with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip().split("\n")


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


registerX = 1
part1_solution = 0
cycle = 1
to_add = None
instructions = iter(puzzle_input)

crt = []

while True:
    if cycle % 40 == 20:  # [20, 60, 100, 140, 180, 220]
        part1_solution += cycle * registerX

    if abs((cycle - 1) % 40 - registerX) in [-1, 0, 1]:
        crt.append("# ")
    else:
        crt.append("  ")

    if to_add:
        registerX += to_add
        to_add = None
    else:
        try:
            instruction = next(instructions)
        except StopIteration:
            break

        if instruction.startswith("addx"):
            to_add = int(instruction.split(" ")[-1])
    cycle += 1

# Part 1 Solution: 17940
print(f"Part 1 Solution: {part1_solution}")

part2_solution = "\n".join("".join(x) for x in chunks(crt, 40))

# Part 2 Solution: ZCBAJFJZ
print(f"Part 2 Solution:\n{part2_solution}")
