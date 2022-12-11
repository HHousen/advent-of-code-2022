from copy import deepcopy
from math import prod
from heapq import nlargest
from operator import mul, add

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip().split("\n\n")

operation_map = {"*": mul, "+": add}
monkeys = []

for monkey_txt in puzzle_input:
    monkey_txt = monkey_txt.split("\n")
    items = [int(x) for x in monkey_txt[1].split(": ")[-1].split(", ")]
    operation = monkey_txt[2].split(" old ")[-1].split()
    if operation[1] != "old":
        operation[1] = int(operation[1])
    test = int(monkey_txt[3].split(" by ")[-1])
    test_true = int(monkey_txt[4][-1])
    test_false = int(monkey_txt[5][-1])
    monkey_dict = {
        "items": items,
        "operation": operation,
        "test": test,
        "test_true": test_true,
        "test_false": test_false,
    }
    monkeys.append(monkey_dict)

# We only care if each worry level is divisible by each monkey's divisor
# (19, 3, 13, etc). For one monkey with a divisor of 19, we could just keep
# track of each item's worry level mod 19. Modular congruence is preserved
# under multiplication and addition. In other words, a + b is divisible by 19
# iff (a % 19) + (b % 19) is divisible by 19. In mathematical notation, this is
# a + b ≡ (a % 19) + (b % 19). For two monkeys with divisors m and n, we have
# (a % (m * n)) % n = a % n and (a % (m * n)) % m = a % m. So, we only need to
# keep track of the worry levels mod the LCM of the monkey's divisors.
# The LCM is the same as the product of the monkey's divisors because all the
# divisors are prime.
# See https://github.com/mebeim/aoc/blob/master/2022/README.md#part-2-10 for
# further explanation.
part2_modulo = prod(monkey["test"] for monkey in monkeys)


def solution(monkeys, part1=True):
    num_inspections = [0] * len(monkeys)
    for _ in range(20 if part1 else 10_000):
        for monkey_idx, monkey in enumerate(monkeys):
            num_inspections[monkey_idx] += len(monkey["items"])
            operation = monkey["operation"]
            for item_worry_level in monkey["items"]:
                op_amount = operation[1]
                if op_amount == "old":
                    op_amount = item_worry_level
                new_worry_level = operation_map[operation[0]](
                    item_worry_level, op_amount
                )
                new_worry_level = (
                    new_worry_level // 3 if part1 else new_worry_level % part2_modulo
                )

                if new_worry_level % monkey["test"] == 0:
                    to_monkey_idx = monkey["test_true"]
                else:
                    to_monkey_idx = monkey["test_false"]
                monkeys[to_monkey_idx]["items"].append(new_worry_level)

            monkey["items"] = []
    return prod(nlargest(2, num_inspections))


part1_solution = solution(deepcopy(monkeys))

# Part 1 Solution: 54752
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solution(monkeys, part1=False)

# Part 2 Solution: 13606755504
print(f"Part 2 Solution: {part2_solution}")
