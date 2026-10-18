import time
from ortools.sat.python import cp_model

def solve_cp_sat(n, print_board=True):
    model = cp_model.CpModel()

    # queens[i] là cột của quân hậu tại hàng i
    queens = []
    for i in range(n):
        queens.append(model.NewIntVar(0, n - 1, f"Q_{i}"))

    # Thêm các quân hậu k cùng 1 hàng
    model.AddAllDifferent(queens)

    # Thêm không cùng đường chéo chính ( queens[i] - i khác nhau ) 
    diag1 = []
    for i in range(n):
        diag1.append(queens[i] - i)
    model.AddAllDifferent(diag1)

    # Thêm không cùng đường chéo phụ ( queens[i] + i khác nhau )
    diag2 = []
    for i in range(n):
        diag2.append(queens[i] + i)
    model.AddAllDifferent(diag2)

    # Solver giải bài toán 
    solver = cp_model.CpSolver()
    
    start_time = time.time()
    status = solver.Solve(model)
    end_time = time.time()
    elapsed = end_time - start_time

    # IN kq
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        if print_board:
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                col = solver.Value(queens[i])
                for j in range(n):
                    if j == col:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        return {
            "n": n,
            "solver": "CP_SAT",
            "status": "SAT",
            "time": round(elapsed, 4),
            "variables": n,
            "clauses": 3,
        }
    else:
        if print_board:
            print("Khong tim thay loi giai!")
        return {
            "n": n,
            "solver": "CP_SAT",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": n,
            "clauses": 3,
        }

if __name__ == "__main__":
    n = 8
    solve_cp_sat(n)
