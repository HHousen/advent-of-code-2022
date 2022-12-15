import re
from itertools import combinations

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()


def manhattan_distance(x, y, a, b):
    return abs(x - a) + abs(y - b)


observations = [
    tuple(map(int, re.findall(r"-?\d+", line))) for line in puzzle_input.split("\n")
]

# Identify the intervals that each sensor covers along y=2,000,000. Save each
# position's x coordinates in this set.
Y_LINE = 2_000_000
positions_covered = set()
for sensor_x, sensor_y, beacon_x, beacon_y in observations:
    # This is the distance from the sensor to its nearest beacon.
    sensor_beacon_distance = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
    # This is the distance from the sensor to the y=2,000,000 line.
    distance_to_y_2million = abs(sensor_y - Y_LINE)
    # Distance covered to the right of the sensor decreases by 1 for each
    # increase by 1 in y. This measures the one sided interval that the sensor
    # covers along y=2,000,000.
    one_sided_interval = sensor_beacon_distance - distance_to_y_2million
    # The sensor doesn't detect any beacons within a distance of
    # `sensor_beacon_distance`. If that distance is greater than or equal to
    # the sensor's distance to y=2,000,000, then the sensor doesn't detect
    # any beacons on some portion of the line at y=2,000,000.
    if sensor_beacon_distance >= distance_to_y_2million:
        positions_covered |= set(
            range(sensor_x - one_sided_interval, sensor_x + one_sided_interval + 1)
        )

# Remove known beacon positions along y=2,000,000.
positions_covered -= set(
    beacon_x for _, _, beacon_x, beacon_y in observations if beacon_y == Y_LINE
)

part1_solution = len(positions_covered)

# Part 1 Solution: 5127797
print(f"Part 1 Solution: {part1_solution}")

# For part 2, there must be a unique answer. Thus, the beacon producing the
# distress signal must be just outside the boundaries of at least two sensors.
# If it were not, then there would be a pocket of possible beacon positions,
# each of which would be valid. The only other possibility is that the beacon
# is in the corner of the 0 to 4,000,000 square search space, but it is not.
BOUNDARY = 4_000_000
# Store each scanner's coordinates and its radius (aka the distance to its
# nearest beacon).
sensor_radiuses = {
    (sensor_x, sensor_y): manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
    for sensor_x, sensor_y, beacon_x, beacon_y in observations
}

# Each scanner creates a diamond search space, of which the boundary is defined
# by 4 lines. We want the lines one space outside, since that is the valid
# area where the missing beacon could be. If a scanner is located at
# (sensor_x, scanner_y) with radius r, then the line segments are:
# y = x + scanner_y - sensor_x + r + 1
# y = x + scanner_y - sensor_x - r - 1
# y = -x + sensor_x + scanner_y + r + 1
# y = -x + sensor_x + scanner_y - r - 1
# Here, we create sets of the coefficients of the lines y=x+a and y=-x+b.
a_coefficients, b_coefficients = set(), set()
for (sensor_x, sensor_y), radius in sensor_radiuses.items():
    a_coefficients.add(sensor_y - sensor_x + radius + 1)
    a_coefficients.add(sensor_y - sensor_x - radius - 1)
    b_coefficients.add(sensor_x + sensor_y + radius + 1)
    b_coefficients.add(sensor_x + sensor_y - radius - 1)


# The lines intersect at ((b-a)/2, (a+b)/2). One of these intersections will
# be the missing scanner location. Essentially, we check each pair of beacons
# compute the intersections just outside their radius, and then check if that
# intersection meets the challenge requirements.
def part2_solve():
    for a in a_coefficients:
        for b in b_coefficients:
            intersection_x, intersection_y = (b - a) // 2, (a + b) // 2
            # Check if the intersection is inside the specified boundary and it
            # is not inside any scanner radius.
            if (
                0 < intersection_x < BOUNDARY
                and 0 < intersection_y < BOUNDARY
                and all(
                    manhattan_distance(
                        intersection_x, intersection_y, sensor_x, sensor_y
                    )
                    > radius
                    for (sensor_x, sensor_y), radius in sensor_radiuses.items()
                )
            ):
                return intersection_x, intersection_y


part2_solution = part2_solve()
part2_solution = 4_000_000 * part2_solution[0] + part2_solution[1]

# Part 2 Solution: 12518502636475
print(f"Part 2 Solution: {part2_solution}")
