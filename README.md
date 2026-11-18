# Multithreaded File Analysis and Performance Evaluation

## 1. Project Overview

This project implements a Sequential File Analyzer and a
Multithreaded File Analyzer using the C programming language
and POSIX threads (pthreads).

The application searches for a target word in multiple text
files and counts its occurrences.

The project also demonstrates race conditions, mutex-based
synchronization, and performance evaluation using different
thread counts and dataset sizes.

## 2. Technologies Used

- C Programming Language
- POSIX Threads (pthreads)
- GCC Compiler
- Ubuntu Linux
- Python 3
- Matplotlib

## 3. Project Features

- Sequential file analysis
- Multithreaded file analysis
- User-defined thread count (1, 2, 4, 8)
- Multiple file processing
- Race condition demonstration
- Mutex-based synchronization
- Performance benchmarking
- Execution time comparison
- Speedup and efficiency calculation
- Performance graphs

## 4. Project Structure

- src/: C source code
- data/: Input datasets
- results/: Benchmark results and graphs
- report/: Technical report
- tests/: Test cases

## 5. Compilation

Open the terminal and navigate to the source directory:

    cd ~/topic3_assignment/src

Compile the Sequential Analyzer:

    gcc -std=c11 -Wall -Wextra -O2 analyzer.c -o analyzer

Compile the Multithreaded Analyzer:

    gcc -std=c11 -Wall -Wextra -O2 -pthread multithreaded_analyzer.c -o multithreaded_analyzer

Compile the Race Condition Program:

    gcc -std=c11 -Wall -Wextra -O0 -pthread race_condition.c -o race_condition

Compile the Mutex Solution:

    gcc -std=c11 -Wall -Wextra -O0 -pthread mutex_solution.c -o mutex_solution

## 6. Running the Programs

### Sequential Analyzer

    ./analyzer WARNING ../data/benchmark_data/file{1..8}.txt

### Multithreaded Analyzer

Run with 1 thread:

    ./multithreaded_analyzer WARNING 1 ../data/benchmark_data/file{1..8}.txt

Run with 2 threads:

    ./multithreaded_analyzer WARNING 2 ../data/benchmark_data/file{1..8}.txt

Run with 4 threads:

    ./multithreaded_analyzer WARNING 4 ../data/benchmark_data/file{1..8}.txt

Run with 8 threads:

    ./multithreaded_analyzer WARNING 8 ../data/benchmark_data/file{1..8}.txt

### Race Condition Demonstration

    ./race_condition

### Mutex Solution

    ./mutex_solution

## 7. Dataset Information

| Dataset | Number of Files | Total Lines |
|---------|-----------------|-------------|
| Small | 8 | 80,000 |
| Medium | 8 | 400,000 |
| Large | 8 | 800,000 |

## 8. Performance Evaluation

Each configuration was measured five times.

The average execution time was calculated and stored in:

- results/repeated_benchmark_raw.csv
- results/average_benchmark.csv

Performance graphs are available in the results directory.

## 9. Performance Metrics

Speedup = Sequential Average Time / Multithreaded Average Time

Efficiency = (Speedup / Number of Threads) * 100

## 10. Limitations

The analyzer uses substring matching. Therefore, it counts
matching character sequences rather than only complete words.

The benchmark execution time includes program startup and
thread creation overhead.

## 11. Author

Student Project
Topic: Multithreaded File Analysis and Performance Evaluation
