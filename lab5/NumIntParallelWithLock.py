from sys import argv, exit
from time import perf_counter
from math import pi as mathPi
import multiprocessing


def main(argv):

    #command line arguments
        
    if len(argv) != 2:
        print('Usage: {} <number of steps>' .format(argv[0]))
        exit(1)
    numberOfSteps = argv[1]
    try:
       numberOfSteps = int(numberOfSteps)
    except ValueError as e:
        print('Integer convertion error: {}' .format(e))
        exit(2)
    if numberOfSteps <= 0:
        print('Steps cannot be non-positive.')
        exit(3)
        
    t1 = perf_counter()
    
    # Get the number of CPU cores
    num_processes = multiprocessing.cpu_count()
    processes = []
    
    # Create a lock
    lock = multiprocessing.Lock()
    
    step = 1.0 / numberOfSteps

    # Create a Value to store pi
    pi_ref = multiprocessing.Value('d', 0.0)
    
    # create processes
    for i in range(num_processes):
        p = multiprocessing.Process(target=calcPiForBlock, args=(i, numberOfSteps, step, num_processes, pi_ref, lock,))
        processes.append(p)
    
    # start processes
    for p in processes:
        p.start()
    
    # wait for processes to finish
    for p in processes:
        p.join()
        
    pi = pi_ref.value * step

    t2 = perf_counter()

    print('Parallel using locks, program results with {} steps' .format(numberOfSteps))
    print('Computed pi = {}' .format(pi))
    print('Difference between estimated pi and math.pi = {}' .format(abs(pi - mathPi)))
    print('Time to compute = {} seconds' .format(t2-t1))

# calculate for each subproblem
def calcPiForBlock(i, steps, step, num_processes, pi, lock):

    local_sum = 0
    
    # Αναγωγή με μοιραζόμενη μεταβλητή και κλείδωμα 
    block = steps//num_processes
    start = i * block
    stop = start + block
    if i==num_processes-1:
        stop = steps

    for j in range(start, stop):
        x = (j + 0.5) * step
        local_sum += 4.0 / (1.0 + x**2)
    
    with lock:
        pi.value += local_sum

if __name__ == '__main__':
    main(argv)