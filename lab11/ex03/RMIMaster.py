# use Python remote object library
import Pyro5.api as pyro

if __name__ == '__main__':
    try:
        # Get the total number of calculation steps from the user
        number_of_steps = int(input("Give total number of calculation steps: "))
    except ValueError:
        print("Wrong data given!")
        exit(1)
        
    ns = pyro.locate_ns()
    # Get the URIs of all registered workers
    worker_uris = [uri for uri in ns.list(prefix="worker_").values()]

    if not worker_uris:
        print("No workers found.")
        exit(-1)
    
    # Create Pyro proxies for each worker
    workers = [pyro.Proxy(uri) for uri in worker_uris]
    tasks = []

    # Divide the calculation work among the workers
    block = number_of_steps // len(workers)
    for i in range(len(workers)):
        start = i * block
        stop = start + block if i < len(workers) - 1 else number_of_steps
        tasks.append([start, stop])
    
    result = 0.0
    results_received = 0
    
    # Iterate over each task and assign it to a worker
    for task in tasks:
        for worker in workers:
            try:                
                # Request the worker to perform the calculation for the assigned task
                task_result = worker.organize_calculation(task[0], task[1])
                result += task_result
                results_received += 1
                break  # Move to the next task after a successful calculation
            except Exception as e:
                print(f"Worker failed with error: {e}")
    
    # Calculate the final result by averaging the results received from workers
    if results_received > 0:
        final_result = result / results_received
    else:
        final_result = 0.0
    
    print("Final result = " + str(final_result))
