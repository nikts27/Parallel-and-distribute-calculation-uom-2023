import threading
import multiprocessing
from time import perf_counter
from math import pi as mathPi
import sys

def main(argv):
    # extract command line arguments
    if len(argv) != 2:
        print('Usage: {} <number of steps>'.format(argv[0]))
        exit(1)
    
    numberOfSteps = argv[1]
    try:
       numberOfSteps = int(numberOfSteps)
    except ValueError as e:
        print('Integer convertion error: {}'.format(e))
        exit(2)
    if numberOfSteps <= 0:
        print('Steps cannot be non-positive.')
        exit(3)
    
    # find the recursive limit
    limit = numberOfSteps // multiprocessing.cpu_count()
    step = 1.0 / numberOfSteps
    
    # create a threading Lock
    lock = threading.Lock()
    # create a shared variable pi
    pi = multiprocessing.Value('d', 0.0)
    
    # start timer
    t1 = perf_counter()

    # create and start the main thread of the program
    t = threading.Thread(target=calcPiRecursive, args=(0, numberOfSteps, step, limit, lock, pi,))
    t.start()
    t.join()
        
    # end timer    
    t2 = perf_counter()

    #get shared variable's value
    pi_value = pi.value
    
    #show results
    print('Recursive program results with {} steps'.format(numberOfSteps))
    print('Computed pi = {}'.format(pi_value))
    print('Difference between estimated pi and math.pi = {}'.format(abs(pi_value - mathPi)))
    print('Time to compute = {} seconds'.format(t2 - t1))

#function that calculates pi using recursive threads
def calcPiRecursive(start, end, step, limit, lock, pi):
    workload = end - start
    if workload <= limit:
        sum = 0
        for i in range(start, end):
            x = (i + 0.5) * step
            sum += 4.0 / (1.0 + x ** 2)
        with lock:
            pi.value += sum * step
    else:
        mid = start + workload // 2
        # create recursive threads
        threadL = threading.Thread(target=calcPiRecursive, args=(start, mid, step, limit, lock, pi))
        threadR = threading.Thread(target=calcPiRecursive, args=(mid, end, step, limit, lock, pi))
        
        threadL.start()
        threadR.start()
        
        threadL.join()
        threadR.join()


if __name__ == '__main__':
    main(sys.argv)