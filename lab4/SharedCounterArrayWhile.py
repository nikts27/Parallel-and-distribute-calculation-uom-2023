import threading

def increase_array(array, end, counter, lock):
    while True:
        with lock:
            if counter[0] >= end:
                break
            array[counter[0]] += 1
            counter[0] += 1

# check if the final array has any errors
def check_array(array, end):
    errors = 0
    
    print("Checking...")
    
    for i in range(end):
        if array[i] != 1:
            errors += 1
            print(str(i) + ": " + str(array[i]) + " should be 1")
    print(str(errors) + " errors.")

if __name__ == '__main__':
    
    threads = []
    numThreads = 4
    end = 10000
    array = [0]*end
    counter = [0]
    lock = threading.Lock()
    
    # Create threads
    for i in range(numThreads):
        t = threading.Thread(target=increase_array, args=(array, end, counter, lock,))
        threads.append(t)
        
    # Start threads
    for t in threads:
        t.start()
        
    # Wait for threads to finish
    for t in threads:
        t.join()
    
    check_array(array, end)