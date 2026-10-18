import time
from ortools.sat.python import cp_model

def solve_cp_sat_bool(n, print_board=True):
    model = cp_model.CpModel()

    # x[i, j] la bien Boolean: 1 neu dat quan hau tai (i, j), 0 neu khong
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = model.NewBoolVar(f"x_{i}_{j}")

    count_constraints = 0

    # Rang buoc 1: Moi hang co dung 1 quan hau (ExactlyOne)
    for i in range(n):
        row_vars = []
        for j in range(n):
            row_vars.append(x[i, j])
        model.AddExactlyOne(row_vars)
        count_constraints += 1

    # Rang buoc 2: Moi cot co dung 1 quan hau (ExactlyOne)
    for j in range(n):
        col_vars = []
        for i in range(n):
            col_vars.append(x[i, j])
        model.AddExactlyOne(col_vars)
        count_constraints += 1

    # Rang buoc 3: Duong cheo chinh co toi da 1 quan hau (AtMostOne)
    for diff in range(-(n - 1), n):
        diag_vars = []
        for i in range(n):
            j = i - diff
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.AddAtMostOne(diag_vars)
            count_constraints += 1

    # Rang buoc 4: Duong cheo phu co toi da 1 quan hau (AtMostOne)
    for total in range(2 * n - 1):
        diag_vars = []
        for i in range(n):
            j = total - i
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.AddAtMostOne(diag_vars)
            count_constraints += 1

    # Solver giai bai toan
    solver = cp_model.CpSolver()

    start_time = time.time()
    status = solver.Solve(model)
    end_time = time.time()
    elapsed = end_time - start_time

    # In ket qua
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        if print_board:
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                for j in range(n):
                    if solver.Value(x[i, j]) == 1:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        return {
            "n": n,
            "solver": "CP_SAT_Bool",
            "status": "SAT",
            "time": round(elapsed, 4),
            "variables": n * n,
            "clauses": count_constraints,
        }
    else:
        if print_board:
            print("Khong tim thay loi giai!")
        return {
            "n": n,
            "solver": "CP_SAT_Bool",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": n * n,
            "clauses": count_constraints,
        }

if __name__ == "__main__":
    n = 8
    solve_cp_sat_bool(n)
