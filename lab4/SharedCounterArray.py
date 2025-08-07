import threading

def increase_array(array, end, lock):
    for i in range(end):
        for j in range(i):
            with lock:
                array[i] += 1

# check if the final array has any errors
def check_array(array, end, numThreads):
    errors = 0
    
    print("Checking...")
    
    for i in range(end):
        if array[i] != numThreads*i:
            errors += 1
            print(str(i) + ": " + str(array[i]) + " should be " + str(numThreads*i))
    print(str(errors) + " errors.")

if __name__ == '__main__':
    
    threads = []
    numThreads = 4
    end = 1000
    array = [0]*end
    lock = threading.Lock()
    
    # Create threads
    for i in range(numThreads):
        t = threading.Thread(target=increase_array, args=(array, end, lock,))
        threads.append(t)
        
    # Start threads
    for t in threads:
        t.start()
    
    # Wait for threads to finish
    for t in threads:
        t.join()
    
    check_array(array, end, numThreads)