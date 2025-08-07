import time
import random
import threading
import multiprocessing

class CyclicBarrier():
    def __init__(self, threads):
        self.totalThreads = threads
        self.arrived = 0
        self.mutex = threading.Semaphore(1)
        self.waiting = threading.Semaphore(0)
        self.leaving = threading.Semaphore(1)
        
    def barrier(self):
        #waiting
        self.mutex.acquire()
        self.arrived = self.arrived + 1
        if self.arrived == self.totalThreads:
            self.waiting.release()
            self.leaving.acquire()
        self.mutex.release()
        self.waiting.acquire()
        self.waiting.release()
        
        #leaving
        self.mutex.acquire()
        self.arrived = self.arrived - 1
        if self.arrived == 0:
            self.waiting.acquire()
            self.leaving.release()
        self.mutex.release()
        self.leaving.acquire()
        self.leaving.release()
        
def test(pid, barrier):
    while True:
        print('Thread ' + str(pid) + ' started')
        barrier.barrier()
        time.sleep(random.random()*1000)
        print('Thread ' + str(pid) + ' reached barrier')
        barrier.barrier()
        print('Thread ' + str(pid) + ' passed barrier')
        barrier.barrier()
        
if __name__ == '__main__':
    
    numThreads = multiprocessing.cpu_count()
    testBarrier = CyclicBarrier(numThreads)
    threads = []
    
    for i in range(numThreads):
        t = threading.Thread(target=test, args=(i, testBarrier,))
        threads.append(t)
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()