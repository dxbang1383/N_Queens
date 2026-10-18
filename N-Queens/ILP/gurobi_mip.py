import time
import gurobipy as gp
from gurobipy import GRB

def solve_gurobi_mip(n, print_board=True):
    # 1. Khoi tao model Gurobi (tat thong bao log de man hinh gon gang)
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    model = gp.Model("N-Queens-Gurobi", env=env)

    # 2. Tao bien nhi phan: x[i, j] = 1 neu dat quan hau tai (i, j), nguoc lai = 0
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # 3. Rang buoc 1: Moi hang co dung 1 quan hau (tong hang = 1)
    for i in range(n):
        row_vars = []
        for j in range(n):
            row_vars.append(x[i, j])
        model.addConstr(gp.quicksum(row_vars) == 1)

    # 4. Rang buoc 2: Moi cot co dung 1 quan hau (tong cot = 1)
    for j in range(n):
        col_vars = []
        for i in range(n):
            col_vars.append(x[i, j])
        model.addConstr(gp.quicksum(col_vars) == 1)

    # 5. Rang buoc 3: Duong cheo chinh co toi da 1 quan hau (tong <= 1)
    for diff in range(-(n - 1), n):
        diag_vars = []
        for i in range(n):
            j = i - diff
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.addConstr(gp.quicksum(diag_vars) <= 1)

    # 6. Rang buoc 4: Duong cheo phu co toi da 1 quan hau (tong <= 1)
    for total in range(2 * n - 1):
        diag_vars = []
        for i in range(n):
            j = total - i
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.addConstr(gp.quicksum(diag_vars) <= 1)

    model.update()
    num_vars = model.NumVars
    num_constrs = model.NumConstrs

    # 7. Solver giai bai toan
    start_time = time.time()
    model.optimize()
    end_time = time.time()
    elapsed = end_time - start_time

    # 8. In ket qua
    if model.status == GRB.OPTIMAL:
        if print_board:
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                for j in range(n):
                    if x[i, j].X > 0.5:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        return {
            "n": n,
            "solver": "Gurobi_MIP",
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
            "solver": "Gurobi_MIP",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_constrs,
        }

if __name__ == "__main__":
    n = 8
    solve_gurobi_mip(n)
