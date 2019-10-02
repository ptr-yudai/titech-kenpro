from minisat import BoolVars, Solver

# Load initial state of sudoku
field = []
with open("field.txt", 'r') as f:
    for line in f:
        field.append(
            list(map(int, line.split(',')))
        )

# Initialize SAT solver
p = BoolVars()
for a in range(9):
    for b in range(9):
        for c in range(9):
            p.add('{}{}{}'.format(a, b, c))
s = Solver(p)

# Identity of cell
for y in range(9):
    for x in range(9):
        s.add([
            p['{}{}{}'.format(y, x, i)] for i in range(9)
        ])

# Uniqueness on row
for y in range(9):
    for i in range(9):
        for x_base in range(9):
            for x in range(x_base + 1, 9):
                s.add([
                    s.Not(p['{}{}{}'.format(y, x_base, i)]),
                    s.Not(p['{}{}{}'.format(y, x     , i)])
                ])

# Uniqueness on column
for x in range(9):
    for i in range(9):
        for y_base in range(9):
            for y in range(y_base + 1, 9):
                s.add([
                    s.Not(p['{}{}{}'.format(y_base, x, i)]),
                    s.Not(p['{}{}{}'.format(y     , x, i)])
                ])

# Uniqueness in block
for m in range(3):
    for n in range(3):
        for i in range(9):
            for w_base in range(9):
                x_base, y_base = n * 3 + w_base % 3, m * 3 + w_base // 3
                for w in range(w_base + 1, 9):
                    x, y = n * 3 + w % 3, m * 3 + w // 3
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, i)]),
                        s.Not(p['{}{}{}'.format(y     , x     , i)])
                    ])

# Input field
for y in range(9):
    for x in range(9):
        if field[y][x] != -1:
            s.add([p['{}{}{}'.format(y, x, field[y][x] - 1)]])

# Solve it!
m = s.solve(p)

if m.is_sat():
    answer = []
    for y in range(9):
        answer.append([])
        for x in range(9):
            for i in range(9):
                if m['{}{}{}'.format(y, x, i)] == True:
                    break
            else:
                print("Something is wrong...")
                exit(1)
            answer[y].append(i + 1)
else:
    print("Solution not found!")
    exit(1)

for y in range(9):
    for x in range(9):
        print("{} ".format(answer[y][x]), end="")
    print("")
