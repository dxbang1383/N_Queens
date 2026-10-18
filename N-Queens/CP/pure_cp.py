import time
from ortools.constraint_solver import pywrapcp

def solve_pure_cp(n, print_board=True):
    # 1. Khoi tao solver CP thuan (Constraint Solver co dien cua Google)
    solver = pywrapcp.Solver("N-Queens-Pure-CP")

    # 2. Tao bien: queens[i] la cot cua quan hau tai hang i
    queens = []
    for i in range(n):
        queens.append(solver.IntVar(0, n - 1, f"Q_{i}"))

    # 3. Rang buoc 1: Khong cung cot
    solver.Add(solver.AllDifferent(queens))

    # 4. Rang buoc 2: Khong cung duong cheo chinh (queens[i] - i khac nhau)
    diag1 = []
    for i in range(n):
        diag1.append(queens[i] - i)
    solver.Add(solver.AllDifferent(diag1))

    # 5. Rang buoc 3: Khong cung duong cheo phu (queens[i] + i khac nhau)
    diag2 = []
    for i in range(n):
        diag2.append(queens[i] + i)
    solver.Add(solver.AllDifferent(diag2))

    # 6. Chien luoc tim kiem (Search Phase): Chon bien chua gan, thu gia tri nho nhat
    db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    # 7. Giai bai toan
    start_time = time.time()
    solver.NewSearch(db)
    found = solver.NextSolution()
    end_time = time.time()
    elapsed = end_time - start_time

    # 8. In ket qua
    if found:
        if print_board:
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                col = queens[i].Value()
                for j in range(n):
                    if j == col:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        solver.EndSearch()
        return {
            "n": n,
            "solver": "Pure_CP",
            "status": "SAT",
            "time": round(elapsed, 4),
            "variables": n,
            "clauses": 3,
        }
    else:
        if print_board:
            print("Khong tim thay loi giai!")
        solver.EndSearch()
        return {
            "n": n,
            "solver": "Pure_CP",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": n,
            "clauses": 3,
        }

if __name__ == "__main__":
    n = 8
    solve_pure_cp(n)
