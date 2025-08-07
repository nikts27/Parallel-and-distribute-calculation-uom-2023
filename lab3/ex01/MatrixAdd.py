# Matrix Addition A = B + C

import multiprocessing
import threading

def addElements(a, b, c, start, stop, size):
    for i in range(start, stop):
        for j in range(size):
            a[i][j] = b[i][j] + c[i][j]
    

if __name__ == '__main__':
    
    threads = []
    num_threads = multiprocessing.cpu_count()
    size = 10
    
    a = [[0.1] * size for i in range(size)]
    b = [[0.3] * size for i in range(size)]
    c = [[0.5] * size for i in range(size)]
    
    block = size//num_threads
    for i in range(num_threads):
        start = i*block
        stop = start+block
        if i==num_threads-1:
            stop = size
        t = threading.Thread(target=addElements, args=(a, b, c, start, stop, size,))
        threads.append(t)
        
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
        
    # For debugging
    for i in range(size):
        for j in range(size):
            print(a[i][j], end=" ")
        print()