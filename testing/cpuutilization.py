import concurrent.futures
import os

def cpu_intensive_task(n):
    # Example CPU-bound task: calculating the nth Fibonacci number
    if n <= 1:
        return n
    else:
        return cpu_intensive_task(n-1) + cpu_intensive_task(n-2)

def main():
    # Get the number of available cores
    num_cores = os.cpu_count()
    print(f"Utilizing all {num_cores} cores")

    # Define the tasks to be executed in parallel
    tasks = [45] * num_cores  # Example: calculating the 45th Fibonacci number on each core

    # Use ProcessPoolExecutor to utilize all cores
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(executor.map(cpu_intensive_task, tasks))

    print("Results:", results)

if __name__ == "__main__":
    main()
