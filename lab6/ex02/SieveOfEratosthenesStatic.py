import sys
import time
import math
import threading
import multiprocessing

# function to find prime numbers within a certain size
def find_primes(start, stop, prime):
    limit = int(math.sqrt(stop) + 1)
    for p in range(2, limit+1):
        if prime[p]:
            for i in range(max(p*p, (start + p - 1) // p * p), stop, p):
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
    
    # find number of threads and block size
    num_threads = multiprocessing.cpu_count()
    threads = []
    block = (size-2)//num_threads
    
    prime = [True] * (size+1)
    prime[:2] = [False, False]
    
    # create threads
    for i in range(num_threads):
        start = i * block + 2
        end = start + block
        if i == num_threads - 1:
            end = size+1
        t = threading.Thread(target=find_primes, args=(start, end, prime,))
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
