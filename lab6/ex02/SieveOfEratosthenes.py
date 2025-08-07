import sys
import time
import math

# function to find prime numbers within a certain size
def find_primes(size):
    prime = [True] * (size + 1)
    prime[:2] = [False, False]
    
    limit = int(math.sqrt(size) + 1)
    for p in range(2, limit+1):
        if prime[p]:
            for i in range(p*p, size+1, p):
                prime[i] = False
    return prime

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
    
    #start timer
    start = time.time()
    
    # call function
    prime = find_primes(size)
                
    # Stop timing
    elapsed_time = (time.time() - start) * 1000
    
    count = 0
    for i in range(2, size+1):
        if prime[i]:
            count += 1
    
    # show results
    print("Number of primes: " + str(count))
    print("Time in ms= " + str(elapsed_time))