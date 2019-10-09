# coding: utf-8
from minisat import BoolVars, Solver

# Initialize SAT solver
# p['xy']: y行x列にz番目のクイーンが存在するか(存在しなければ0)
p = BoolVars()
for a in range(8):
    for b in range(8):
        for c in range(9):
            p.add('{}{}{}'.format(a, b, c))
s = Solver(p)

# Identity of cell
# y行x列には必ず0〜8のいずれかが当てはまる
for y in range(8):
    for x in range(8):
        s.add([p['{}{}{}'.format(y, x, n)] for n in range(9)])

# Uniqueness of cell
# y行x列は2つ以上の状態を取らない
for y in range(8):
    for x in range(8):
        for n_base in range(9):
            for n in range(9):
                if n_base == n: continue
                s.add([
                    s.Not(p['{}{}{}'.format(y, x, n_base)]),
                    s.Not(p['{}{}{}'.format(y, x, n)])
                ])

# Identity of n-th queen
# 盤面のどこかに1〜8のqueenが存在する
for n in range(1, 9):
    s.add([
        p['{}{}{}'.format(i // 8, i % 8, n)]
        for i in range(8 * 8)
    ])

# Uniqueness of n-th queen
# あるセルにn番のqueenが存在したとき、別のセルにn番のqueenは存在しない
for n in range(1, 9):
    for y_base in range(8):
        for x_base in range(8):
            for y in range(y_base + 1, 8):
                for x in range(x_base + 1, 8):
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, n)]),
                        s.Not(p['{}{}{}'.format(y, x, n)])
                    ])

# Main
for y_base in range(8):
    for x_base in range(8):
        for n_base in range(1, 9):
            # Horizontal check
            # y行x列にqueenが存在したとき、その行には別のqueenが存在しない
            for x in range(8):
                for n in range(1, 9):
                    if n == n_base: continue
                    if x == x_base: continue
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, n_base)]),
                        s.Not(p['{}{}{}'.format(y_base, x, n)])
                    ])
            # Vertical check
            # y行x列にqueenが存在したとき、その列には別のqueenが存在しない
            for y in range(8):
                for n in range(1, 9):
                    if n == n_base: continue
                    if y == y_base: continue
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, n_base)]),
                        s.Not(p['{}{}{}'.format(y, x_base, n)])
                    ])
            # Diagonal check
            # y行x列にqueenが存在したとき、その斜め方向には別のqueenが存在しない
            for n in range(1, 9):
                if n == n_base: continue
                for delta in range(-7, 8):
                    x, y = x_base + delta, y_base - delta
                    if x < 0 or x > 7: continue
                    if y < 0 or y > 7: continue
                    if x == x_base and y == y_base: continue
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, n_base)]),
                        s.Not(p['{}{}{}'.format(y, x, n)])
                    ])
                for delta in range(-7, 8):
                    x, y = x_base + delta, y_base + delta
                    if x < 0 or x > 7: continue
                    if y < 0 or y > 7: continue
                    if x == x_base and y == y_base: continue
                    s.add([
                        s.Not(p['{}{}{}'.format(y_base, x_base, n_base)]),
                        s.Not(p['{}{}{}'.format(y, x, n)])
                    ])

# Solve it!
m = s.solve(p)

if m.is_sat():
    answer = []
    for y in range(8):
        answer.append([])
        for x in range(8):
            for n in range(9):
                if m['{}{}{}'.format(y, x, n)] == True:
                    break
            else:
                print("Something is wrong...")
                exit(1)
            answer[y].append(False if n == 0 else True)
else:
    print("Solution not found!")
    exit(1)

for y in range(8):
    for x in range(8):
        print("{}".format('Q' if answer[y][x] else '.'), end="")
    print("")
