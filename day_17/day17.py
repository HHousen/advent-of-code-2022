with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

jet_directions = puzzle_input
direction_to_coord = {"<": -1, ">": 1}
TOWER_WIDTH = 7

# The rock configurations given in the challenge description.
rocks = [
    [(2, 0), (3, 0), (4, 0), (5, 0)],  # horizontal line
    [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)],  # plus
    [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],  # L
    [(2, 0), (2, 1), (2, 2), (2, 3)],  # vertical line
    [(2, 0), (2, 1), (3, 0), (3, 1)],  # square
]


def solve(num_rocks):
    # Store the tower as a set of coordinates filled in. The tower starts as
    # just a floor along the width of the tower.
    tower = {(x, 0) for x in range(TOWER_WIDTH)}
    # Keep track of the state of the tower each time a new piece is placed. If
    # we encounter the same state again, we have a cycle and can skip forward
    # as close as possible to the destination number of rocks dropped.
    potential_cycle_cache = {}
    # The current jet we are at in the jet of jets.
    jet_idx = 0
    # The greatest y-coordinate in `tower`.
    tower_height = 0
    # The number of rocks dropped so far.
    step = 0
    # The amount of height found from a detected cycle. This is added to the
    # final `tower_height`. This makes it easy to keep building the tower
    # without changing `tower_height` midway through execution.
    additional_height = 0
    # Keep track if a cycle has been detected yet. If a cycle is detected, we
    # no longer need to search for cycles (which costs a substantial amount of
    # computation as the tower grows large) since repeating one cycle can get
    # very close to the desired number of rocks placed.
    cycle_detected = False
    # Keep track of the greatest y-coordinate in each column of the tower in
    # order to build a key to detect cycles.
    tower_top = [0] * TOWER_WIDTH

    # Keep dropping rocks until the desired number of rocks have been dropped.
    while step < num_rocks:
        # The current rock being dropped.
        rock_idx = step % len(rocks)

        # If we have not yet detected a cycle, check if the current game state
        # has been seen before. If it has skip forward, otherwise store the
        # current game state so we can check against it in the future.
        if not cycle_detected:
            # Compute the shape of the top of the tower stored as a 7-tuple of
            # the height of each column relative to the `tower_height`.
            top_of_tower = tuple(x - tower_height for x in tower_top)

            # The `key` is the current state of the game. If we have
            # encountered this same tuple before, then we can repeat those
            # moves to get as close as possible to the desired `num_rocks`.
            # This will not actually generate a completely unique state since
            # pieces can fall and get tucked under the top of the tower, thus
            # changing the state but not modifying the `top_of_tower`. However,
            # this is exceptionally rare and doesn't happen in the AoC inputs.
            key = (rock_idx, jet_idx, top_of_tower)
            if key in potential_cycle_cache:
                # We've seen this key before so a cycle has been detected.
                cycle_detected = True
                # `cycle_tower_height` and `cycle_step` are the tower height
                # and step where the cycle started.
                cycle_tower_height, cycle_step = potential_cycle_cache[key]
                steps_remaining = num_rocks - step
                length_of_cycle = step - cycle_step
                # How many times we can repeat this cycle to get as close as
                # possible to `num_rocks` dropped.
                num_repeats = steps_remaining // (length_of_cycle)
                # Fast forward the step to the step after teh maximum number of
                # cycles have been completed.
                step += (length_of_cycle) * num_repeats
                # Keep track of how much height is gained by repeating this
                # cycle for the maximum number of times.
                additional_height += (tower_height - cycle_tower_height) * num_repeats
            else:
                # If we haven't seen this state before, store the current state.
                potential_cycle_cache[key] = (tower_height, step)

        # Get the rock being dropped this iteration.
        rock = rocks[rock_idx]
        new_y = tower_height + 4
        # Move to rock from y=0 to the appropriate height to drop.
        rock = [(x, y + new_y) for x, y in rock]

        while True:
            # Get the change in the rock's x-coordinate caused by the jet.
            jet_direction = jet_directions[jet_idx]
            jet_direction = direction_to_coord[jet_direction]
            # Increment the jet index, but keep it in bounds.
            jet_idx = (jet_idx + 1) % len(jet_directions)
            # Try moving the rock specified by the jet direction.
            new_rock = [(x + jet_direction, y) for x, y in rock]
            # If the rock goes out of bounds of the tower or collides with an
            # existing block, don't move the rock.
            if (not all(0 <= x < TOWER_WIDTH for x, _ in new_rock)) or any(
                coord in tower for coord in new_rock
            ):
                new_rock = rock
            else:
                rock = new_rock
            # Try moving the rock down.
            down_rock = [(x, y - 1) for x, y in rock]
            # If the moved down rock collides with another rock, then the rock
            # has settled and can be added to the tower.
            if any(coord in tower for coord in down_rock):
                # Add rock to the tower.
                tower.update(rock)
                # Compute the new height of the tower, which is either the old
                # tower height (if the rock landed below the top of the tower)
                # or the maximum height of the rock (if the rock landed on top
                # of the tower).
                rock_max = max(y for _, y in rock)
                tower_height = max(rock_max, tower_height)
                # Update the maximum height of each column of the tower.
                for x, y in rock:
                    tower_top[x] = max(tower_top[x], y)
                break
            # If the rock didn't collide when moving down, then update the
            # rock's position and continue to the next iteration.
            rock = down_rock
        step += 1
    # Return the height of the final tower, including any height skipped due to
    # fast forwarding with a cycle.
    return tower_height + additional_height


part1_solution = solve(2022)

# Part 1 Solution: 3197
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solve(int(1e12))

# Part 2 Solution: 1568513119571
print(f"Part 2 Solution: {part2_solution}")
