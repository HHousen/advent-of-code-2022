import json

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

pairs = [
    [json.loads(x) for x in pair.split("\n")] for pair in puzzle_input.split("\n\n")
]


def compare(left, right):
    # This syntax can be improved with Python 3.10's match statement.
    if type(left) == int and type(right) == int:
        return left - right
    elif type(left) == int and type(right) == list:
        return compare([left], right)
    elif type(left) == list and type(right) == int:
        return compare(left, [right])
    elif type(left) == list and type(right) == list:
        for l, r in zip(left, right):
            comparison = compare(l, r)
            if comparison:
                return comparison
        return len(left) - len(right)


valid_indicies = []
for idx, (first_packet, second_packet) in enumerate(pairs):
    idx += 1
    if compare(first_packet, second_packet) < 0:
        valid_indicies.append(idx)

part1_solution = sum(valid_indicies)

# Part 1 Solution: 5198
print(f"Part 1 Solution: {part1_solution}")


def divider_index(packets, target):
    # Only care about the locations of the divider packets and not the
    # locations of any other packet. Thus, compare the divider target to each
    # other packet and see where it should go. Use sum to count number of
    # packets that we iterated through to find the correct index.
    # Another option is to use `sorted` with `key=itertools.cmp_to_key(compare)`
    # and then find the index of the divider packets in the sorted list.
    return sum(compare(packet, target) <= 0 for packet in packets)


packets = [item for sublist in pairs for item in sublist]
two = [[2]]
six = [[6]]
packets.extend([two, six])

part2_solution = divider_index(packets, two) * divider_index(packets, six)

# Part 2 Solution: 22344
print(f"Part 2 Solution: {part2_solution}")
