with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

rucksacks = puzzle_input.split("\n")


def prioritize(item):
    return ord(item) - ord("`") if ord(item) > ord("`") else ord(item) - ord("@") + 26


total = 0
for rucksack in rucksacks:
    compartment1, compartment2 = (
        rucksack[: len(rucksack) // 2],
        rucksack[len(rucksack) // 2 :],
    )
    intersection = set(compartment1) & set(compartment2)
    priority = prioritize(intersection.pop())
    total += priority

part1_solution = total

# Part 1 Solution: 8243
print(f"Part 1 Solution: {part1_solution}")

total = 0
for idx in range(0, len(rucksacks), 3):
    common_item = (
        set(rucksacks[idx]) & set(rucksacks[idx + 1]) & set(rucksacks[idx + 2])
    )
    priority = prioritize(common_item.pop())
    total += priority

part2_solution = total

# Part 2 Solution: 2631
print(f"Part 2 Solution: {part2_solution}")
