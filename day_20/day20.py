from copy import deepcopy

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

numbers = list(enumerate(int(x) for x in puzzle_input.split("\n")))
num_numbers = len(numbers)


def solve(numbers, num_mixes=1):
    # Multiplying by `num_mixes` causes the array we iterate over to be a copy
    # of `numbers`.
    for idx, number in numbers * num_mixes:
        # Get the current location of `number` in the list since it may have
        # been moved during a previous iteration.
        current_idx = numbers.index((idx, number))
        # Remove the `number` from the list of numbers.
        numbers.pop(current_idx)
        # Insert the `number` back into the list at the position
        # `previous_idx + number`. This will move the number left or right
        # relative to its current position in the list by a number of positions
        # equal to the value of the `number`.
        new_idx = (current_idx + number) % (num_numbers - 1)
        numbers.insert(new_idx, (idx, number))

    new_numbers = [number for _, number in numbers]
    zero_idx = new_numbers.index(0)

    return sum(new_numbers[(zero_idx + i) % num_numbers] for i in [1000, 2000, 3000])


part1_solution = solve(deepcopy(numbers))

# Part 1 Solution: 6387
print(f"Part 1 Solution: {part1_solution}")

numbers = [(idx, number * 811589153) for idx, number in numbers]
part2_solution = solve(numbers, num_mixes=10)

# Part 2 Solution: 2455057187825
print(f"Part 2 Solution: {part2_solution}")
