import threading

#method that each thread uses to print the multiples of a number
def print_multiples(num):
    for i in range(20):
        print("Thread " + str(num) + ": " + str(i+1) + " * " + str(num) + " = " + str((i+1)*num))

if __name__ =="__main__":
    
    threads = []
    print('Print 20 first multipliers of numbers 1 to 10')
    
    #create the threads
    for i in range(10):
        t = threading.Thread(target=print_multiples, args=(i+1,))
        threads.append(t)
        t.start()
        
    #wait for threads to finish
    for t in threads:
        t.join()
        
    print('Finished!')