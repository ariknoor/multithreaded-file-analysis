import csv
import matplotlib.pyplot as plt

datasets = {
    "Small": {},
    "Medium": {},
    "Large": {}
}

with open("results/average_benchmark.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset = row["dataset"]
        config = row["configuration"]
        time = float(row["average_ms"])

        datasets[dataset][config] = time

configurations = ["Sequential", "1", "2", "4", "8"]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for ax, (dataset, results) in zip(axes, datasets.items()):
    times = [results[c] for c in configurations]

    ax.bar(configurations, times)
    ax.set_title(f"{dataset} Dataset")
    ax.set_xlabel("Execution Configuration")
    ax.set_ylabel("Average Execution Time (ms)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.suptitle(
    "Sequential vs Multithreaded File Analyzer Performance",
    fontsize=14
)

plt.tight_layout()

plt.savefig("results/performance_graph.png", dpi=300)

print("Performance graph created successfully.")
print("Saved at: results/performance_graph.png")

plt.show()
