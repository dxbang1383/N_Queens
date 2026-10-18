import time
from docplex.cp.model import CpoModel

def solve_cplex_cp(n, print_board=True):
    model = CpoModel(name="N-Queens")

    # queens[i] la cot cua quan hau tai hang i
    queens = []
    for i in range(n):
        queens.append(model.integer_var(0, n - 1, f"Q_{i}"))

    # Cac quan hau khong cung 1 cot
    model.add(model.all_diff(queens))

    # Khong cung duong cheo chinh (queens[i] - i khac nhau)
    diag1 = []
    for i in range(n):
        diag1.append(queens[i] - i)
    model.add(model.all_diff(diag1))

    # Khong cung duong cheo phu (queens[i] + i khac nhau)
    diag2 = []
    for i in range(n):
        diag2.append(queens[i] + i)
    model.add(model.all_diff(diag2))

    # Solver giai bai toan
    start_time = time.time()
    try:
        sol = model.solve(LogVerbosity="Quiet")
        end_time = time.time()
        elapsed = end_time - start_time

        # In ket qua
        if sol and sol.is_solution():
            if print_board:
                print(f"Thoi gian giai: {elapsed:.4f} giay")
                print("Ban co ket qua:")
                for i in range(n):
                    col = sol.get_value(queens[i])
                    for j in range(n):
                        if j == col:
                            print("Q", end=" ")
                        else:
                            print(".", end=" ")
                    print()
            return {
                "n": n,
                "solver": "CPLEX_CP",
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
                "solver": "CPLEX_CP",
                "status": "UNSAT",
                "time": round(elapsed, 4),
                "variables": n,
                "clauses": 3,
            }
    except Exception as e:
        if print_board:
            print(f"Loi khi goi CPLEX CP: {e}")
        return {
            "n": n,
            "solver": "CPLEX_CP",
            "status": "ERROR",
            "time": None,
            "variables": n,
            "clauses": 3,
        }

if __name__ == "__main__":
    n = 8
    solve_cplex_cp(n)
