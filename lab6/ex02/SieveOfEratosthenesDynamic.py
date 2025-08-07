import sys
import time
import math
import threading
import multiprocessing

def getTask(tasksAssigned, totalTasks):
    with tasksAssigned.get_lock():
        tasksAssigned.value += 1
        if tasksAssigned.value < totalTasks:
            return tasksAssigned.value
        else:
            return -1

# function to find prime numbers within a certain size
def find_primes(size, tasksAssigned, prime):
    limit = int(math.sqrt(size) + 1)
    element = getTask(tasksAssigned, limit + 1)
    while element >= 0:
        if prime[element]:
            for i in range(element * element, size + 1, element):
                prime[i] = False
        element = getTask(tasksAssigned, limit + 1)

if __name__ == "__main__":
    
    # command line arguments
    if len(sys.argv) != 2:
        print("Usage: python SieveOfEratosthenes.py <size>") 
        sys.exit(1)
    
    #check if given size is a correct argument
    try:
        int(sys.argv[1])
    except ValueError:
        print("Integer argument exception")
        sys.exit(2)
    
    size = int(sys.argv[1])
    if size <= 0:
        print("Size should be positive integer")
        sys.exit(3)
    
    # find number of threads
    num_threads = multiprocessing.cpu_count()
    threads = []
    
    prime = bytearray([True] * (size + 1))
    prime[:2] = [False, False]
    
    # create a threading value to share the tasksAssigned value among the threads
    tasksAssigned = multiprocessing.Value('i', 1)
    
    # create threads
    for i in range(num_threads):
        t = threading.Thread(target=find_primes, args=(size, tasksAssigned, prime,))
        threads.append(t)
        
    #start timer
    start = time.time()
    
    # start threads
    for t in threads:
        t.start()
    
    # wait for threads to end
    for t in threads:
        t.join()
                
    # Stop timing
    elapsed_time = (time.time() - start) * 1000
    
    count = 0
    prime_list = list(prime)
    for i in range(2, size+1):
        if prime_list[i]:
            count += 1   
             
    # show results
    print("Number of primes: " + str(count))
    print("Time in ms= " + str(elapsed_time))
