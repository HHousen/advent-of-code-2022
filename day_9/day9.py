with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

moves = [x.split(" ") for x in puzzle_input.split("\n")]
directions = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0


rope = [[0, 0] for _ in range(10)]

visited = [set(), set()]
previous_direction = None
for direction, distance in moves:
    distance = int(distance)

    for _ in range(distance):
        coord_change = directions[direction]
        rope[0][0] += coord_change[0]
        rope[0][1] += coord_change[1]
        # Update the position of every knot in the rope (excluding the head,
        # since we just updated its position).
        for rope_idx in range(1, 10):
            knot1_position = rope[rope_idx - 1]
            knot2_position = rope[rope_idx]
            # Change in coordinates between the last knot and the current knot.
            # For the first iteration, the last knot is the head and thus we
            # update the second knot's position based on the head's change in
            # position.
            dx = knot1_position[0] - knot2_position[0]
            dy = knot1_position[1] - knot2_position[1]
            # If moving tail in a straight line...
            if dx == 0 or dy == 0:
                # Update the one coordinate of the tail depending on the
                # direction moved.
                if abs(dx) > 1:
                    rope[rope_idx][0] += sign(dx)
                if abs(dy) > 1:
                    rope[rope_idx][1] += sign(dy)
            # If the tail is moving diagonally...
            # (A distance of (1, 1) is diagonally adjacent and thus not far enough.)
            elif not (abs(dx) == 1 and abs(dy) == 1):
                # Update both coordinates in the direction moved.
                rope[rope_idx][0] += sign(dx)
                rope[rope_idx][1] += sign(dy)
        # Keep track of the positions that the first knot (excluding the head
        # of the rope) visits.
        visited[0].add(tuple(rope[1]))
        # Keep track of the positions that the last knot visits.
        visited[1].add(tuple(rope[-1]))

part1_solution = len(visited[0])

# Part 1 Solution: 6026
print(f"Part 1 Solution: {part1_solution}")

part2_solution = len(visited[1])

# Part 2 Solution: 2273
print(f"Part 2 Solution: {part2_solution}")

# This was my original solution to part 1. However, my modified solution for
# part 2 is capable of solving part 1. This original solution is left here
# in case it is useful later in a way that part 2's solution is not.
# visited = set()
# head_position = (0, 0)
# tail_position = (0, 0)
# previous_direction = None
# for direction, distance in moves:
#     distance = int(distance)

#     for _ in range(distance):
#         previous_head_position = head_position
#         head_position = tuple(
#             head_position[i] + directions[direction][i] for i in range(2)
#         )
#         head_tail_distance = [
#             abs(head_position[i] - tail_position[i]) for i in range(2)
#         ]
#         if any(x > 1 for x in head_tail_distance):
#             tail_position = previous_head_position
#         visited.add(tail_position)


# part1_solution = len(visited)
