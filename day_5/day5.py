from copy import deepcopy

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

crates_raw, moves = puzzle_input.split("\n\n")
crates_raw = crates_raw.split("\n")[:-1]
moves = moves.split("\n")


crates = [[] for _ in range(9)]

for line in crates_raw:
    for idx, crate_value in enumerate(line[1::4]):
        if crate_value != " ":
            crates[idx].append(crate_value)

crates = [list(reversed(x)) for x in crates]


def solution(crates, part_2=False):
    for move_line in moves:
        _, num, _, source, _, destination = move_line.split(" ")
        num = int(num)
        source = int(source) - 1
        destination = int(destination) - 1
        crates_to_move = crates[source][-num:]
        if part_2:
            moving = list(crates_to_move)
        else:
            moving = list(reversed(crates_to_move))
        crates[destination].extend(moving)
        del crates[source][-num:]

    crates_on_top = [x[-1] for x in crates]
    return "".join(crates_on_top)


part1_solution = solution(deepcopy(crates))

# Part 1 Solution: BSDMQFLSP
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solution(crates, part_2=True)

# Part 2 Solution: PGSQBFLDP
print(f"Part 2 Solution: {part2_solution}")
