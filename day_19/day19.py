import re
import numpy as np
from tqdm import tqdm

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

blueprints = [
    tuple(map(int, re.findall(r"-?\d+", line))) for line in puzzle_input.split("\n")
]

# Weight production twice as much as the inventory when pruning states.
key = lambda a: tuple(a[0] + [x * 2 for x in a[1]])


def prune(states):
    # Increase the number of states left over after pruning if this doesn't
    # work on your input.
    return sorted(states, key=key, reverse=True)[:500]


def solve_blueprint(blueprint, time):
    # Choices has the cost and production of each robot type in the order
    # geode, obsidian, clay, ore, and no robot.
    choices = [
        ((0, 0, 0, blueprint[0]), (0, 0, 0, 1)),
        ((0, 0, 0, blueprint[1]), (0, 0, 1, 0)),
        ((0, 0, blueprint[3], blueprint[2]), (0, 1, 0, 0)),
        ((0, blueprint[5], 0, blueprint[4]), (1, 0, 0, 0)),
        ((0, 0, 0, 0), (0, 0, 0, 0)),
    ]
    choices = [np.array(x) for x in choices]
    start_state = (np.array([0, 0, 0, 0]), np.array([0, 0, 0, 1]))
    # States has tuples of (inventory, production).
    states = [start_state]
    best_total_geodes = 0
    for _ in range(time):
        new_states = []
        for inventory, current_production in states:
            for cost, additional_production in choices:
                if all(cost <= inventory):
                    new_production = current_production + additional_production
                    new_inventory = inventory + current_production - cost

                    new_states.append((new_inventory, new_production))
                    best_total_geodes = max(best_total_geodes, new_inventory[0])
        states = prune(new_states)
    return best_total_geodes


part1_solution = 0
for blueprint_idx, *blueprint in tqdm(blueprints, desc="Part 1"):
    part1_solution += solve_blueprint(blueprint, 24) * blueprint_idx

# Part 1 Solution: 1653
print(f"Part 1 Solution: {part1_solution}")

part2_solution = 1
for blueprint_idx, *blueprint in tqdm(blueprints[:3], desc="Part 2"):
    part2_solution *= solve_blueprint(blueprint, 32)

# Part 2 Solution: 4212
print(f"Part 2 Solution: {part2_solution}")
