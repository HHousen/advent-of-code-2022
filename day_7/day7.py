from collections import defaultdict

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()


current_directory = ["/"]
folders = defaultdict(int)
for line in puzzle_input.split("\n"):
    if line[0] == "$":
        if line[2:4] == "cd":
            argument = line[5:]
            if argument == "..":
                current_directory.pop()
            elif argument == "/":
                current_directory = ["/"]
            else:
                current_directory.append(argument)
    else:
        size, name = line.split()
        if size != "dir":
            for idx in range(len(current_directory)):
                path = "-".join(current_directory[: idx + 1])
                folders[path] += int(size)

part1_solution = sum(x for x in folders.values() if x <= 100_000)

# Part 1 Solution: 1084134
print(f"Part 1 Solution: {part1_solution}")

unused_space = 70_000_000 - folders["/"]
space_needed = 30_000_000 - unused_space

part2_solution = min(size for size in folders.values() if size >= space_needed)

# Part 2 Solution: 6183184
print(f"Part 2 Solution: {part2_solution}")
