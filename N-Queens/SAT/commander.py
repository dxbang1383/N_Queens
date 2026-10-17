from pysat.solvers import Glucose3
import math

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
# Với commander: chia các biến thành nhóm (kích thước 3), mỗi nhóm có 1 biến chỉ huy
def at_most_one(variables):
    l = len(variables)
    if l <= 1: return []
    if l == 2: return [[- variables[0], - variables[1]]]
    else:
        clauses = []
        commanders = []
        group_size = 3

        # Chia các biến thành các nhóm nhỏ cỡ 3
        for i in range(0, l, group_size):
            group = []
            for j in range(i, min(i + group_size, l)):
                group.append(variables[j])

            # Nếu nhóm chỉ có 1 biến thì đưa thẳng vào làm commander
            if len(group) == 1:
                commanders.append(group[0])
            else:
                # Tạo 1 biến chỉ huy cho nhóm
                c = new_var()
                commanders.append(c)

                # Dòng 1: Các biến trong cùng nhóm không được cùng là true
                k = len(group)
                for g1 in range(k):
                    for g2 in range(g1 + 1, k):
                        clauses.append([- group[g1], - group[g2]])

                # Dòng 2: Biến trong nhóm là true thì biến chỉ huy phải là true (x -> c)
                for x in group:
                    clauses.append(implies(x, c))

        # Dòng 3: Đệ quy ép các biến chỉ huy chỉ có tối đa 1 biến nhận true
        if len(commanders) > 1:
            clauses = clauses + at_most_one(commanders)

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

if __name__ == "__main__":
    n = 8
    clauses = convert_to_clause(n)

    print(f"So luong menh de la : {len(clauses)}")
    print(clauses)

    solver = Glucose3()

    for c in clauses:
        solver.add_clause(c)

    if solver.solve():
        model = solver.get_model()

        for i in range(n):
            for j in range(n):
                if var(i, j, n) in model:
                    print("Q", end=" ")
                else:
                    print(".", end=" ")
            print()

    else:
        print("Khong tim thay loi giai!")
