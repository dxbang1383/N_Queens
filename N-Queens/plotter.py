import os
import csv
import matplotlib.pyplot as plt

# 1. Bang mau va ky hieu scatter cho tung bo giai (chia theo nhom de de quan sat)
SOLVER_STYLES = {
    # Nhom SAT: Tong mau do / cam / vang
    "SAT_Binomial":   {"color": "#D32F2F", "marker": "o", "label": "SAT: Binomial"},
    "SAT_Binary":     {"color": "#F57C00", "marker": "s", "label": "SAT: Binary"},
    "SAT_Sequential": {"color": "#FFA000", "marker": "^", "label": "SAT: Sequential"},
    "SAT_Commander":  {"color": "#E64A19", "marker": "v", "label": "SAT: Commander"},
    "SAT_Product":    {"color": "#C2185B", "marker": "D", "label": "SAT: Product"},

    # Nhom CP: Tong mau xanh la / xanh ngoc
    "CP_SAT":         {"color": "#2E7D32", "marker": "*", "label": "CP: OR-Tools CP-SAT"},
    "Pure_CP":        {"color": "#689F38", "marker": "X", "label": "CP: Pure Backtracking"},
    "CPLEX_CP":       {"color": "#00796B", "marker": "P", "label": "CP: IBM CPLEX CP"},
    "CP_SAT_Bool":    {"color": "#00897B", "marker": "d", "label": "CP: CP-SAT Boolean"},

    # Nhom ILP / MIP: Tong mau xanh duong / tim
    "Gurobi_MIP":     {"color": "#1565C0", "marker": "p", "label": "ILP: Gurobi MIP"},
    "CPLEX_MIP":      {"color": "#512DA8", "marker": "h", "label": "ILP: CPLEX MIP"},
    "SCIP_MIP":       {"color": "#5C6BC0", "marker": "<", "label": "ILP: SCIP MIP"},
}


def read_data_from_csv(csv_path):
    # Kiem tra file CSV co ton tai khong
    if not os.path.exists(csv_path):
        print(f"Loi: Khong tim thay file {csv_path}!")
        return None

    # Khoi tao dictionary de luu du lieu
    data = {}

    f = open(csv_path, mode="r", encoding="utf-8")
    reader = csv.DictReader(f)

    for row in reader:
        solver = row["Solver"]
        status = row["Status"]

        if solver not in data:
            data[solver] = {
                "n_list": [],
                "time_list": [],
                "clause_list": [],
                "var_list": []
            }

        # Chi lay nhung lan giai thanh cong (SAT) de ve bieu do
        if status == "SAT":
            try:
                n_val = int(row["N"].strip())
                time_val = float(row["Time_Seconds"].strip())
                clause_val = int(row["Constraints_or_Clauses"].strip())
                var_val = int(row["Variables"].strip())

                # Thoi gian neu bang 0.0 thi gan muc toi thieu 0.0001s de bieu dien duoc tren thang log
                if time_val <= 0.0:
                    time_val = 0.0001

                data[solver]["n_list"].append(n_val)
                data[solver]["time_list"].append(time_val)
                data[solver]["clause_list"].append(clause_val)
                data[solver]["var_list"].append(var_val)
            except Exception:
                continue

    f.close()
    return data


def plot_scatter_runtime(data, output_dir):
    # 1. Khoi tao khung ve
    plt.figure(figsize=(11, 7))

    all_n = []

    # 2. Ve cac diem scatter va duong dan huong mo cho tung solver
    for solver_name in data:
        metrics = data[solver_name]
        x_vals = metrics["n_list"]
        y_vals = metrics["time_list"]

        if len(x_vals) > 0:
            for val in x_vals:
                if val not in all_n:
                    all_n.append(val)

            # Lay mau sac va ky hieu marker
            style = SOLVER_STYLES.get(solver_name, {"color": "gray", "marker": "o", "label": solver_name})
            color = style["color"]
            marker = style["marker"]
            label = style["label"]

            # Ve diem scatter noi bat: size 75, vien den, do mo 0.85
            plt.scatter(
                x_vals,
                y_vals,
                s=75,
                color=color,
                marker=marker,
                edgecolors="black",
                linewidths=0.7,
                alpha=0.85,
                label=label,
                zorder=4
            )

            # Ve duong net cham mo noi cac diem de mat de theo doi xu huong
            plt.plot(
                x_vals,
                y_vals,
                color=color,
                linestyle=":",
                linewidth=1.2,
                alpha=0.5,
                zorder=3
            )

    # 3. Thiet lap truc va luoi
    all_n.sort()
    plt.yscale("log")
    if len(all_n) > 0:
        plt.xticks(all_n, fontsize=11)
    plt.yticks(fontsize=11)

    plt.xlabel("Kich thuoc ban co (N)", fontsize=13, fontweight="bold")
    plt.ylabel("Thoi gian giai - giay (Thang Logarit)", fontsize=13, fontweight="bold")
    plt.title("Bieu do Scatter: So sanh thoi gian giai N-Queens giua cac Solver", fontsize=14, fontweight="bold")

    # Luoi grid phu ro rang
    plt.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5, zorder=1)

    # Chu thich Legend 2 cot ben ngoai hoac phia tren
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), ncol=1, fontsize=9.5, frameon=True)

    plt.tight_layout()

    # 4. Luu anh
    out_file = os.path.join(output_dir, "scatter_runtime.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print("[+] Da luu bieu do scatter thoi gian tai:", out_file)


def plot_scatter_clauses(data, output_dir):
    # 1. Khoi tao khung ve
    plt.figure(figsize=(11, 7))

    all_n = []

    # 2. Ve cac diem scatter the hien so menh de / rang buoc
    for solver_name in data:
        metrics = data[solver_name]
        x_vals = metrics["n_list"]
        y_vals = metrics["clause_list"]

        if len(x_vals) > 0:
            for val in x_vals:
                if val not in all_n:
                    all_n.append(val)

            style = SOLVER_STYLES.get(solver_name, {"color": "gray", "marker": "o", "label": solver_name})
            color = style["color"]
            marker = style["marker"]
            label = style["label"]

            plt.scatter(
                x_vals,
                y_vals,
                s=75,
                color=color,
                marker=marker,
                edgecolors="black",
                linewidths=0.7,
                alpha=0.85,
                label=label,
                zorder=4
            )

            plt.plot(
                x_vals,
                y_vals,
                color=color,
                linestyle=":",
                linewidth=1.2,
                alpha=0.5,
                zorder=3
            )

    all_n.sort()
    plt.yscale("log")
    if len(all_n) > 0:
        plt.xticks(all_n, fontsize=11)
    plt.yticks(fontsize=11)

    plt.xlabel("Kich thuoc ban co (N)", fontsize=13, fontweight="bold")
    plt.ylabel("So luong menh de / rang buoc (Thang Logarit)", fontsize=13, fontweight="bold")
    plt.title("Bieu do Scatter: Quy mo mo hinh (Clauses / Constraints)", fontsize=14, fontweight="bold")

    plt.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5, zorder=1)
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), ncol=1, fontsize=9.5, frameon=True)

    plt.tight_layout()

    out_file = os.path.join(output_dir, "scatter_clauses.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print("[+] Da luu bieu do scatter so menh de tai:", out_file)


def plot_scatter_runtime_vs_clauses(data, output_dir):
    # Bieu do scatter tuong quan: Truc X la so menh de, truc Y la thoi gian giai
    plt.figure(figsize=(11, 7))

    for solver_name in data:
        metrics = data[solver_name]
        x_vals = metrics["clause_list"]
        y_vals = metrics["time_list"]

        if len(x_vals) > 0:
            style = SOLVER_STYLES.get(solver_name, {"color": "gray", "marker": "o", "label": solver_name})
            color = style["color"]
            marker = style["marker"]
            label = style["label"]

            plt.scatter(
                x_vals,
                y_vals,
                s=80,
                color=color,
                marker=marker,
                edgecolors="black",
                linewidths=0.7,
                alpha=0.85,
                label=label,
                zorder=4
            )

            # Duong noi giua cac moc N cua cung 1 solver
            plt.plot(
                x_vals,
                y_vals,
                color=color,
                linestyle=":",
                linewidth=1.0,
                alpha=0.4,
                zorder=3
            )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("So luong menh de / rang buoc (Thang Logarit)", fontsize=13, fontweight="bold")
    plt.ylabel("Thoi gian giai - giay (Thang Logarit)", fontsize=13, fontweight="bold")
    plt.title("Bieu do Scatter Tuong quan: Quy mo mo hinh vs Thoi gian giai", fontsize=14, fontweight="bold")

    plt.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5, zorder=1)
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), ncol=1, fontsize=9.5, frameon=True)

    plt.tight_layout()

    out_file = os.path.join(output_dir, "scatter_runtime_vs_clauses.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print("[+] Da luu bieu do scatter tuong quan tai:", out_file)


def run_plotter():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "figures")
    csv_file = os.path.join(current_dir, "benchmark_results_5.csv")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Dang doc du lieu tu file:", csv_file)
    data = read_data_from_csv(csv_file)

    if data:
        print("Dang ve cac bieu do scatter chuan dep...")
        plot_scatter_runtime(data, output_dir)
        plot_scatter_clauses(data, output_dir)
        plot_scatter_runtime_vs_clauses(data, output_dir)
        print("\n[HOAN THANH] Toan bo anh bieu do scatter da luu tai thu muc:", output_dir)


if __name__ == "__main__":
    run_plotter()
