import os
import shutil
import matplotlib.pyplot as plt
import pandas as pd

# Create output directories for generated graphs
os.makedirs("plots", exist_ok=True)
os.makedirs(os.path.join("frontend", "plots"), exist_ok=True)

# Define dataset from empirical observation benchmark tables
data = {
    "Workload": ["W1", "W2", "W3", "W4", "W5"],
    "Concurrent_Requests": [1, 2, 4, 8, 16],
    # Response Times (ms)
    "Student_RespTime": [6.82, 7.15, 8.42, 10.12, 12.85],
    "Internship_RespTime": [5.95, 6.30, 7.60, 9.80, 13.40],
    "Application_RespTime": [12.40, 13.85, 16.20, 21.45, 28.90],
    # Throughput (RPS)
    "Student_RPS": [3.4, 6.9, 14.2, 28.5, 54.2],
    "Internship_RPS": [3.5, 7.2, 15.0, 29.8, 56.5],
    "Application_RPS": [3.1, 6.2, 12.8, 24.6, 46.2],
    # CPU Utilization (%)
    "Student_CPU": [1.20, 2.80, 5.40, 9.60, 16.40],
    "Internship_CPU": [1.10, 2.40, 4.80, 8.90, 15.10],
    "Application_CPU": [2.50, 4.60, 8.80, 16.70, 27.30],
    # Memory Utilization (MB)
    "Student_Mem": [52.40, 52.80, 53.50, 54.10, 55.20],
    "Internship_Mem": [51.80, 52.10, 52.60, 53.20, 54.00],
    "Application_Mem": [56.20, 56.90, 57.80, 58.50, 59.80],
}

df = pd.DataFrame(data)

# Styling setup
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
markers = {"Student": "o", "Internship": "s", "Application": "^"}
colors = {
    "Student": "#2563eb",      # Cobalt Blue
    "Internship": "#059669",   # Emerald Green
    "Application": "#d97706"   # Amber/Orange
}

def plot_metric(y_student, y_internship, y_application, title, ylabel, filename):
    plt.figure(figsize=(9, 5.5), dpi=300)
    
    plt.plot(
        df["Concurrent_Requests"], df[y_student],
        marker=markers["Student"], color=colors["Student"], linewidth=2.2, markersize=7,
        label="Student Service (:8002)"
    )
    plt.plot(
        df["Concurrent_Requests"], df[y_internship],
        marker=markers["Internship"], color=colors["Internship"], linewidth=2.2, markersize=7,
        label="Internship Service (:8003)"
    )
    plt.plot(
        df["Concurrent_Requests"], df[y_application],
        marker=markers["Application"], color=colors["Application"], linewidth=2.2, markersize=7,
        label="Application Service (:8004 - Inter-Service Validation)"
    )
    
    plt.title(title, fontsize=13, fontweight="bold", pad=14, color="#1e293b")
    plt.xlabel("Concurrent Requests (Users)", fontsize=11, labelpad=10, fontweight="medium", color="#334155")
    plt.ylabel(ylabel, fontsize=11, labelpad=10, fontweight="medium", color="#334155")
    plt.xticks(df["Concurrent_Requests"], [f"{w} ({u}u)" for w, u in zip(df["Workload"], df["Concurrent_Requests"])], fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=9.5, loc="best")
    plt.tight_layout()
    
    target_path = os.path.join("plots", filename)
    plt.savefig(target_path)
    plt.close()
    
    # Also sync into frontend/plots
    frontend_path = os.path.join("frontend", "plots", filename)
    shutil.copy2(target_path, frontend_path)
    print(f"Generated & Synced: plots/{filename} -> frontend/plots/{filename}")

# 1. Concurrent Requests vs Average Response Time
plot_metric(
    "Student_RespTime", "Internship_RespTime", "Application_RespTime",
    "Workload Concurrency vs. Average Response Time",
    "Average Response Time (ms)",
    "1_response_time.png"
)

# 2. Concurrent Requests vs Throughput
plot_metric(
    "Student_RPS", "Internship_RPS", "Application_RPS",
    "Workload Concurrency vs. Throughput (RPS)",
    "Throughput (Requests Per Second)",
    "2_throughput.png"
)

# 3. Concurrent Requests vs CPU Utilization
plot_metric(
    "Student_CPU", "Internship_CPU", "Application_CPU",
    "Workload Concurrency vs. CPU Utilization (%)",
    "CPU Utilization (%)",
    "3_cpu_utilization.png"
)

# 4. Concurrent Requests vs Memory Utilization
plot_metric(
    "Student_Mem", "Internship_Mem", "Application_Mem",
    "Workload Concurrency vs. Memory Utilization (MB)",
    "Memory Footprint (MB)",
    "4_memory_utilization.png"
)

print("\nAll benchmark plots generated and synchronized with frontend/plots/ successfully!")
