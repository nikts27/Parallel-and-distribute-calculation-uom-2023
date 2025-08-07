# Vector Addition a = b + c 

import multiprocessing
import threading

def addElements(a, b, c, start, stop):
    for i in range(start, stop):
        a[i] = b[i] + c[i]
            

if __name__ == '__main__':
    
    threads = []
    num_threads = multiprocessing.cpu_count()
    size = 10000
        
    a = []
    b = []
    c = []
    
    for i in range(size):
        a.append(0)
        b.append(1)
        c.append(0.5)
    
        
    block = size//num_threads
    for i in range(num_threads):
        start = i*block
        stop = start+block
        if i==num_threads-1:
            stop = size
        t = threading.Thread(target=addElements, args=(a, b, c, start, stop,))
        threads.append(t)
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
    
    # for debugging
    for i in range(size):
        print(a[i])