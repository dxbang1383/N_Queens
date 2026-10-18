import time
from pysat.solvers import Glucose3

next_var = 1

# Biểu diễn suy ra 
def implies(a, b):
    return [-a, b]

def new_var():
    global next_var
    current_id = next_var
    next_var = next_var + 1
    return current_id

def var(i, j, n):
    return i * n + j + 1

def at_least_one(variables):
    return [variables]

# Đầu vào var : là list chứa các ô có ràng buộc AMO với nhau 
# Với sequential: tạo thêm l-1 biến mới làm đèn tín hiệu
def at_most_one(variables):
    l = len(variables)
    if l <= 1: return []
    if l == 2: return [[-variables[0], -variables[1]]]
    else:
        clauses = []
        new_param = []

        # Tạo thêm l-1 biến mới làm đèn 
        for i in range(l - 1):
            new_param.append(new_var())

        # Dòng biến 1 là điều kiện để ràng buộc các biến mới ai -> si
        for i in range(l - 1):
            clauses.append(implies(variables[i], new_param[i]))

        # Dòng biến 2 là điều kiện dẫn si -> si+1
        for i in range(l - 2):
            clauses.append(implies(new_param[i], new_param[i + 1]))

        # Dòng biến 3 là biến chặn si -> - ai+1 
        for i in range(l - 1):
            clauses.append(implies(new_param[i], -variables[i + 1]))

        return clauses

# EO = AMO + ALO
def exactly_one(variables):
    return at_least_one(variables) + at_most_one(variables)

# Chuyển bài toán thành mệnh đề 
def convert_to_clause(n):
    global next_var
    next_var = n * n + 1
    clauses = []
    ## Chuyển hàng thành clauses
    for i in range(n): 

        # Lấy các chỉ số của các ô trên 1 hàng 
        row_vars = []
        for j in range(n):
            row_vars.append(var(i, j, n))
            
        clauses = clauses + exactly_one(row_vars)

    ## Chuyển cột thành claudes
    for j in range(n):

        col_vars = []

        for i in range(n):
            col_vars.append(var(i, j, n))

        clauses = clauses + exactly_one(col_vars)

    ## Chuyển các đường chéo thành clauses (AMO)
    
    # 1. Đường chéo xuôi song song với (0, 0) và (n, n)
    for diff in range(-(n - 2), n - 1):
        x_vars = []
        
        for i in range(n):
            j = i - diff
            
            if j >= 0 and j < n:
                x_vars.append(var(i, j, n))
                
        clauses = clauses + at_most_one(x_vars)

    #2 Đường chéo song song với (n, 0) (0, n)
    for sum in range(1, 2 * n - 2):
        x_vars = []

        for i in range(n):
            j = sum - i

            if j >= 0 and j < n:
                x_vars.append(var(i, j, n))

        clauses = clauses + at_most_one(x_vars)

    return clauses

def solve_sequential(n, print_board=True):
    t0 = time.time()
    clauses = convert_to_clause(n)
    num_clauses = len(clauses)
    num_vars = next_var - 1

    solver = Glucose3()
    for c in clauses:
        solver.add_clause(c)

    sat = solver.solve()
    t1 = time.time()
    elapsed = t1 - t0

    if sat:
        model = solver.get_model()
        if print_board:
            print(f"So luong menh de la : {num_clauses}")
            print(f"Thoi gian giai: {elapsed:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                for j in range(n):
                    if var(i, j, n) in model:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        solver.delete()
        return {
            "n": n,
            "solver": "SAT_Sequential",
            "status": "SAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_clauses,
        }
    else:
        if print_board:
            print("Khong tim thay loi giai!")
        solver.delete()
        return {
            "n": n,
            "solver": "SAT_Sequential",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_clauses,
        }

if __name__ == "__main__":
    n = 8
    solve_sequential(n)