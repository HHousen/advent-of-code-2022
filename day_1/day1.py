with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read()

elves = puzzle_input.split("\n\n")
elf_calories = [
    sum(int(num_calories) for num_calories in elf.strip().split("\n")) for elf in elves
]
part1_solution = max(elf_calories)

# Part 1 Solution: 70374
print(f"Part 1 Solution: {part1_solution}")

elf_calories = sorted(elf_calories)
part2_solution = sum(elf_calories[-3:])

# Part 2 Solution: 204610
print(f"Part 2 Solution: {part2_solution}")
