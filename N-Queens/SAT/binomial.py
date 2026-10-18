import time
from pysat.solvers import Glucose3

## Quy ước : 
# + Bàn cờ giả định trong đầu là đánh số từ 0 nhưng khi mã hóa thì trả về chỉ số được cộng thêm 1 để né (0,0)

# Trả về chi số của ma trận 2 chiều trong mảng 1 chiều 
def var(i, j, n):
    return i * n + j + 1

# Đầu vào var : là list chứa các ô ( mảng 2d) có ràng buộc ALO với nhau vd: [1, 2, 3, 4]
def at_least_one(variables):
    return [variables]

# Đầu vào var : là list chứa các ô có ràng buộc AMO với nhau 
# Tức là 2 cặp bất kì trong biến đều không cùng có giá trị true (and của 2 cặp = false)
# OR của phủ định 2 mệnh đề -a or -b
def at_most_one(variables):
    clauses = []
    k = len(variables)

    for i in range(k): 
        for j in range(i + 1, k):
            clauses.append([-variables[i], -variables[j]])

    return clauses

# EO = AMO + ALO
def exactly_one(variables):
    return at_least_one(variables) + at_most_one(variables)

# Chuyển bài toán thành mệnh đề 
def convert_to_clause(n):
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

def solve_binomial(n, print_board=True):
    t0 = time.time()
    clauses = convert_to_clause(n)
    num_clauses = len(clauses)
    num_vars = n * n

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
            "solver": "SAT_Binomial",
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
            "solver": "SAT_Binomial",
            "status": "UNSAT",
            "time": round(elapsed, 4),
            "variables": num_vars,
            "clauses": num_clauses,
        }

if __name__ == "__main__":
    n = 8
    solve_binomial(n)