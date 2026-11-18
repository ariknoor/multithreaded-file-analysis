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
        datasets[row["dataset"]][row["configuration"]] = float(row["average_ms"])

configurations = ["Sequential", "1", "2", "4", "8"]

for dataset, results in datasets.items():

    times = [results[c] for c in configurations]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(configurations, times)

    plt.title(f"{dataset} Dataset - Performance Comparison")
    plt.xlabel("Execution Configuration")
    plt.ylabel("Average Execution Time (ms)")

    plt.bar_label(bars, fmt="%.2f ms", padding=4)

    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    filename = f"results/{dataset.lower()}_performance.png"

    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Created: {filename}")

print("\nAll individual graphs created successfully.")
