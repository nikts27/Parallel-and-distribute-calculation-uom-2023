import sys
import time
import math
import threading
import multiprocessing

# function to find prime numbers within a certain size
def find_primes(rank, size, num_threads, prime):
    limit = int(math.sqrt(size) + 1)
    for p in range(rank, limit+1, num_threads):
        if prime[p]:
            for i in range(max(p*p, (rank + p - 1) // p * p), size+1, p):
                prime[i] = False

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
    if size<=0:
        print("Size should be positive integer")
        sys.exit(3)
    
    # find number of threads
    num_threads = multiprocessing.cpu_count()
    threads = []
    
    prime = [True] * (size+1)
    prime[:2] = [False, False]
    
    # create threads
    for i in range(num_threads):
        t = threading.Thread(target=find_primes, args=(i, size, num_threads, prime,))
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
    
    count = sum(1 for p in prime if p)
    
    # show results
    print("Number of primes: " + str(count))
    print("Time in ms= " + str(elapsed_time))