import time
from ortools.linear_solver import pywraplp

def solve_scip_mip(n, print_board=True):
    # 1. Khoi tao solver MIP/ILP (su dung SCIP backend ma nguon mo)
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        print("Khong the khoi tao solver SCIP!")
        return {
            "n": n,
            "solver": "SCIP_MIP",
            "status": "ERROR",
            "time": None,
            "variables": 0,
            "clauses": 0,
        }

    # 2. Tao bien nhi phan: x[i, j] = 1 neu dat quan hau tai (i, j), nguoc lai = 0
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = solver.BoolVar(f"x_{i}_{j}")

    # 3. Rang buoc 1: Moi hang co dung 1 quan hau (tong hang = 1)
    for i in range(n):
        row_vars = []
        for j in range(n):
            row_vars.append(x[i, j])
        solver.Add(solver.Sum(row_vars) == 1)

    # 4. Rang buoc 2: Moi cot co dung 1 quan hau (tong cot = 1)
    for j in range(n):
        col_vars = []
        for i in range(n):
            col_vars.append(x[i, j])
        solver.Add(solver.Sum(col_vars) == 1)

    # 5. Rang buoc 3: Duong cheo chinh co toi da 1 quan hau (tong <= 1)
    for diff in range(-(n - 1), n):
        diag_vars = []
        for i in range(n):
            j = i - diff
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            solver.Add(solver.Sum(diag_vars) <= 1)

    # 6. Rang buoc 4: Duong cheo phu co toi da 1 quan hau (tong <= 1)
    for total in range(2 * n - 1):
        diag_vars = []
        for i in range(n):
            j = total - i
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            solver.Add(solver.Sum(diag_vars) <= 1)

    num_vars = solver.NumVariables()
    num_constrs = solver.NumConstraints()

    # 7. Solver giai bai toan
    start_time = time.time()
    status = solver.Solve()
    end_time = time.time()
    elapsed = end_time - start_time

    # 8. In ket qua
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        if print_board:
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                for j in range(n):
                    if x[i, j].solution_value() > 0.5:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        return {
            "n": n,
            "solver": "SCIP_MIP",
            "status": "SAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_constrs,
        }
    else:
        if print_board:
            print("Khong tim thay loi giai!")
        return {
            "n": n,
            "solver": "SCIP_MIP",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_constrs,
        }

if __name__ == "__main__":
    n = 8
    solve_scip_mip(n)
