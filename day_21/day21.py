from sympy import Symbol
from sympy.solvers import solve
from sympy import sympify

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().rstrip()

equations = [x.replace(":", "=") for x in puzzle_input.split("\n")]
num_equations = len(equations)

idx = 0
root = 0
# Continuously loop over the equations until we know the value of `root`.
while root == 0:
    # For each expression, try to execute it. Eventually, `root` will have a
    # value once all the variables it depends on have been evaluated.
    try:
        exec(equations[idx % num_equations])
    # Ignore all exceptions from variables not being defined.
    except:
        pass
    idx += 1


part1_solution = int(root)

# Part 1 Solution: 223971851179174
print(f"Part 1 Solution: {part1_solution}")

values = {"humn": "x"}
# Loop until we have parsed all of the equations.
while len(values) < len(equations):
    for equation in equations:
        name = equation[:4]
        value = equation[6:]
        if name == "root":
            value1, operator, value2 = value.split()
            if value1 in values and value2 in values:
                values[name] = f"{values[value1]}={values[value2]}"
        if name in values:
            continue
        if value.isnumeric():
            values[name] = int(value)
        else:
            value1, operator, value2 = value.split()
            if value1 in values and value2 in values:
                values[name] = f"({values[value1]}{operator}{values[value2]})"
                if "x" not in values[name]:
                    values[name] = int(eval(values[name]))


equation = values["root"]
print(f"Solving: {equation}")

x = Symbol("x")
# Rearrange the equation to be equal to zero for sympy.
lhs, rhs = equation.split("=")
equation = f"{lhs}-({rhs})"
# Solve the equation for `x`.
solution = solve(sympify(equation), x)[0]

part2_solution = solution

# Part 2 Solution: 3379022190351
print(f"Part 2 Solution: {part2_solution}")
