import sys
import math
import time
import multiprocessing
import concurrent.futures

def main(argv):
    # Command line arguments
    if len(argv) != 2:
        print('Usage: {} <number of steps>'.format(argv[0]))
        sys.exit(1)

    try:
        numberOfSteps = int(argv[1])
    except ValueError as e:
        print('Integer conversion error: {}'.format(e))
        sys.exit(2)

    if numberOfSteps <= 0:
        print('Steps cannot be non-positive.')
        sys.exit(3)

    t1 = time.perf_counter()

    # Get the number of CPU cores
    num_processes = multiprocessing.cpu_count()

    # Split the workload among processes
    block_size = numberOfSteps // num_processes
    step = 1.0 / numberOfSteps

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Map the calculation function to the executor
        results = executor.map(calcPiForBlock, range(num_processes), [block_size] * num_processes, 
                               [numberOfSteps] * num_processes, [step] * num_processes)

    # Sum up the results
    pi = sum(results) * step

    t2 = time.perf_counter()

    print('Sequential program results with {} steps'.format(numberOfSteps))
    print('Computed pi =', pi)
    print('Difference between estimated pi and math.pi =', abs(pi - math.pi))
    print('Time to compute = {} seconds'.format(t2 - t1))


def calcPiForBlock(i, block_size, steps, step):
    local_sum = 0
    start = i * block_size
    stop = min((i + 1) * block_size, steps)

    for j in range(start, stop):
        x = (j + 0.5) * step
        local_sum += 4.0 / (1.0 + x ** 2)

    return local_sum


if __name__ == '__main__':
    main(sys.argv)