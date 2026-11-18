import csv

data = {
    "Small": {
        "Sequential": [19976130, 19096259, 18766474, 19734369, 18916964],
        "1": [21119950, 20002304, 19146152, 21202979, 18495539],
        "2": [8760839, 8800172, 7949847, 7750234, 9152294],
        "4": [13590558, 13331782, 15032246, 12932151, 14157826],
        "8": [13472836, 12174127, 12167304, 11681550, 12315029]
    },
    "Medium": {
        "Sequential": [53523921, 51479271, 48262279, 39103540, 27271160],
        "1": [58380110, 46472922, 46651485, 51069883, 28875961],
        "2": [37980258, 30835199, 30194795, 31566409, 28535691],
        "4": [24205128, 22770388, 27876086, 21950277, 20993960],
        "8": [27138652, 21776972, 20547309, 23895588, 20106668]
    },
    "Large": {
        "Sequential": [81267194, 46613213, 40705199, 40763516, 61068965],
        "1": [83079259, 77502485, 50369735, 45678671, 45278376],
        "2": [57450173, 56943406, 44213769, 34940453, 33420464],
        "4": [43070929, 27632052, 26878246, 36338901, 22993465],
        "8": [28788561, 27508068, 19430464, 25418942, 20192963]
    }
}

line_counts = {
    "Small": 80000,
    "Medium": 400000,
    "Large": 800000
}

with open("../results/repeated_benchmark_raw.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "dataset", "total_lines", "configuration",
        "run", "elapsed_nanoseconds"
    ])

    for dataset, configs in data.items():
        for config, runs in configs.items():
            for run_number, elapsed in enumerate(runs, 1):
                writer.writerow([
                    dataset, line_counts[dataset],
                    config, run_number, elapsed
                ])

with open("../results/average_benchmark.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "dataset", "total_lines", "configuration",
        "average_ms", "speedup", "efficiency_percent"
    ])

    for dataset, configs in data.items():
        sequential_avg = sum(configs["Sequential"]) / 5

        for config, runs in configs.items():
            average = sum(runs) / 5
            speedup = sequential_avg / average

            if config == "Sequential":
                efficiency = 100.0
            else:
                efficiency = speedup / int(config) * 100

            writer.writerow([
                dataset,
                line_counts[dataset],
                config,
                round(average / 1_000_000, 3),
                round(speedup, 3),
                round(efficiency, 2)
            ])

print("Benchmark CSV files created successfully.")
print("Raw measurements: 75")
print("\nAverage execution times:")

for dataset, configs in data.items():
    print(f"\n{dataset}:")
    for config, runs in configs.items():
        average_ms = sum(runs) / 5 / 1_000_000
        print(f"{config}: {average_ms:.3f} ms")
