import os
import sys
import csv
import json
import subprocess

# 1. Danh sach 12 bo giai can thu nghiem: (Ten_Hien_Thi, Module, Ham)
SOLVERS = [
    # Nhom SAT (5 cach ma hoa)
    ("SAT_Binomial", "SAT.binomial", "solve_binomial"),
    ("SAT_Binary", "SAT.binary", "solve_binary"),
    ("SAT_Sequential", "SAT.sequential", "solve_sequential"),
    ("SAT_Commander", "SAT.commander", "solve_commander"),
    ("SAT_Product", "SAT.product", "solve_product"),

    # Nhom CP (4 bo giai va mo hinh)
    ("CP_SAT", "CP.cp_sat", "solve_cp_sat"),
    ("Pure_CP", "CP.pure_cp", "solve_pure_cp"),
    ("CPLEX_CP", "CP.cplex_cp", "solve_cplex_cp"),
    ("CP_SAT_Bool", "CP.cp_sat_bool", "solve_cp_sat_bool"),

    # Nhom ILP / MIP (3 bo giai)
    ("Gurobi_MIP", "ILP.gurobi_mip", "solve_gurobi_mip"),
    ("CPLEX_MIP", "ILP.cplex_mip", "solve_cplex_mip"),
    ("SCIP_MIP", "ILP.scip_mip", "solve_scip_mip"),
]

# 2. Bo kich thuoc N 
N_LIST = [4, 8, 16, 32, 40, 50, 60, 70, 80, 90, 100]

# 3. Thoi gian toi da cho moi phep thu (giay)
TIMEOUT = 30.0

def run_solver_single(module_name, func_name, n):
    # Chay bo giai trong tien trinh rieng de co the ngat chinh xac khi qua thoi gian
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    code = f"import sys, json; sys.path.insert(0, str()); from {module_name} import {func_name}; res = {func_name}({n}, False); print(json.dumps(res))"
    cmd = [sys.executable, "-c", code]

    try:
        proc = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True, timeout=TIMEOUT)
        output_text = proc.stdout.strip()
        
        if len(output_text) > 0:
            ket_qua = json.loads(output_text)
            return ket_qua
        else:
            return {
                "n": n,
                "solver": func_name,
                "status": "ERROR",
                "time": None,
                "variables": None,
                "clauses": None,
            }
            
    except subprocess.TimeoutExpired:
        # Neu vuot qua TIMEOUT giay, he dieu hanh se ngat process ngay lap tuc
        return {
            "n": n,
            "solver": func_name,
            "status": "TIMEOUT",
            "time": TIMEOUT,
            "variables": None,
            "clauses": None,
        }
    except Exception as e:
        return {
            "n": n,
            "solver": func_name,
            "status": "ERROR",
            "time": None,
            "variables": None,
            "clauses": None,
        }


def run_benchmark():
    # 1. Chuan bi file CSV de luu ket qua
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "benchmark_results.csv")

    f = open(csv_file, mode="w", newline="", encoding="utf-8")
    writer = csv.writer(f)

    # 2. Ghi dong tieu de (Header)
    header = ["N", "Solver", "Status", "Time_Seconds", "Variables", "Constraints_or_Clauses"]
    writer.writerow(header)

    print("=" * 70)
    print("BAT DAU THUC NGHIEM SO SANH 12 BO GIAI N-QUEENS")
    print("Danh sach N thu nghiem:", N_LIST)
    print("Gioi han thoi gian:", TIMEOUT, "giay")
    print("=" * 70)

    # 3. Vong lap chay tung kich thuoc N
    for n in N_LIST:
        print(f"\n>>> Dang thu nghiem voi N = {n}:")

        for item in SOLVERS:
            ten_solver = item[0]
            ten_module = item[1]
            ten_ham = item[2]

            ket_qua = run_solver_single(ten_module, ten_ham, n)

            trang_thai = ket_qua["status"]
            thoi_gian = ket_qua["time"]
            so_bien = ket_qua["variables"]
            so_menh_de = ket_qua["clauses"]

            # In thong tin tien do ra man hinh
            if trang_thai == "SAT":
                print(f"  [+] {ten_solver:<16}: {thoi_gian:.4f}s (Vars: {so_bien}, Clauses/Constrs: {so_menh_de})")
            elif trang_thai == "TIMEOUT":
                print(f"  [-] {ten_solver:<16}: TIMEOUT (qua {TIMEOUT}s)")
            else:
                print(f"  [x] {ten_solver:<16}: {trang_thai}")

            # Ghi ket qua vao file CSV ngay lap tuc
            dong_du_lieu = [n, ten_solver, trang_thai, thoi_gian, so_bien, so_menh_de]
            writer.writerow(dong_du_lieu)
            f.flush()

    f.close()
    print("\n" + "=" * 70)
    print("Hoan thanh thu nghiem! Ket qua da duoc luu vao:", csv_file)
    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
