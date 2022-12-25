with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip().splitlines()


def to_decimal(number):
    if not number:
        return 0
    start = number[0:-1]
    last = number[-1]
    last = "=-012".index(last) - 2
    return to_decimal(start) * 5 + last


def to_snafu(number):
    if not number:
        return ""
    return to_snafu((number + 2) // 5) + "=-012"[(number + 2) % 5]


decimal_numbers = [to_decimal(snafu_number) for snafu_number in puzzle_input]
part1_solution = to_snafu(sum(decimal_numbers))

# Part 1 Solution: 2-02===-21---2002==0
print(f"Part 1 Solution: {part1_solution}")

part2_solution = 0

print(f"No Part 2 for the 25th challenge.")
