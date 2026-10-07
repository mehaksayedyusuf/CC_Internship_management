import os
import matplotlib.pyplot as plt
import pandas as pd

# Create output directory for generated graphs
os.makedirs("plots", exist_ok=True)

# Define dataset from observation tables
data = {
    "Workload": ["W1", "W2", "W3", "W4", "W5"],
    "Concurrent_Requests": [1, 2, 4, 8, 16],
    # Response Times (ms)
    "Student_RespTime": [10.53, 10.45, 10.27, 10.19, 10.40],
    "Internship_RespTime": [9.25, 8.96, 9.40, 11.23, 11.74],
    "Application_RespTime": [7.98, 8.95, 9.15, 9.41, 10.51],
    # Throughput (RPS)
    "Student_RPS": [3.1, 5.8, 12.4, 25.6, 50.6],
    "Internship_RPS": [3.1, 6.4, 13.6, 26.4, 50.8],
    "Application_RPS": [3.0, 6.9, 11.6, 25.7, 50.4],
    # CPU Utilization (%)
    "Student_CPU": [1.0, 2.60, 5.14, 3.93, 3.93],
    "Internship_CPU": [1.70, 2.55, 5.54, 10.87, 19.20],
    "Application_CPU": [2.10, 2.98, 4.94, 11.11, 16.31],
    # Memory Utilization (MB)
    "Student_Mem": [55.20, 55.48, 55.14, 55.14, 55.14],
    "Internship_Mem": [53.95, 54.29, 54.48, 55.46, 56.14],
    "Application_Mem": [53.17, 53.90, 55.03, 54.98, 54.16],
}

df = pd.DataFrame(data)

# Styling setup
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
markers = {"Student": "o", "Internship": "s", "Application": "^"}
colors = {"Student": "#1f77b4", "Internship": "#ff7f0e", "Application": "#2ca02c"}

# Helper function to generate standardized plots
def plot_metric(y_student, y_internship, y_application, title, ylabel, filename):
    plt.figure(figsize=(8, 5), dpi=300)
    
    plt.plot(df["Concurrent_Requests"], df[y_student], marker=markers["Student"], color=colors["Student"], linewidth=2, label="Student Service")
    plt.plot(df["Concurrent_Requests"], df[y_internship], marker=markers["Internship"], color=colors["Internship"], linewidth=2, label="Internship Service")
    plt.plot(df["Concurrent_Requests"], df[y_application], marker=markers["Application"], color=colors["Application"], linewidth=2, label="Application Service")
    
    plt.title(title, fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Concurrent Requests (Users)", fontsize=10, labelpad=8)
    plt.ylabel(ylabel, fontsize=10, labelpad=8)
    plt.xticks(df["Concurrent_Requests"])
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", filename))
    plt.close()
    print(f"Generated: plots/{filename}")

# 1. Concurrent Requests vs Average Response Time
plot_metric(
    "Student_RespTime", "Internship_RespTime", "Application_RespTime",
    "Concurrent Requests vs. Average Response Time",
    "Average Response Time (ms)",
    "1_response_time.png"
)

# 2. Concurrent Requests vs Throughput
plot_metric(
    "Student_RPS", "Internship_RPS", "Application_RPS",
    "Concurrent Requests vs. Throughput (RPS)",
    "Throughput (Requests Per Second)",
    "2_throughput.png"
)

# 3. Concurrent Requests vs CPU Utilization
plot_metric(
    "Student_CPU", "Internship_CPU", "Application_CPU",
    "Concurrent Requests vs. CPU Utilization (%)",
    "CPU Utilization (%)",
    "3_cpu_utilization.png"
)

# 4. Concurrent Requests vs Memory Utilization
plot_metric(
    "Student_Mem", "Internship_Mem", "Application_Mem",
    "Concurrent Requests vs. Memory Utilization (MB)",
    "Memory Utilization (MB)",
    "4_memory_utilization.png"
)

print("\nAll benchmark plots saved successfully in the 'plots/' directory!")
