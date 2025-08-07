import time
import random
import multiprocessing

class CyclicBarrier():
    def __init__(self, processes):
        self.totalProcesses = processes
        self.arrived = multiprocessing.Value('i',0)
        self.mutex = multiprocessing.Semaphore(1)
        self.waiting = multiprocessing.Semaphore(0)
        self.leaving = multiprocessing.Semaphore(1)
        
    def barrier(self):
        #waiting
        self.mutex.acquire()
        self.arrived.value = self.arrived.value + 1
        if self.arrived.value == self.totalProcesses:
            self.waiting.release()
            self.leaving.acquire()
        self.mutex.release()
        self.waiting.acquire()
        self.waiting.release()
        
        #leaving
        self.mutex.acquire()
        self.arrived.value = self.arrived.value - 1
        if self.arrived.value == 0:
            self.waiting.acquire()
            self.leaving.release()
        self.mutex.release()
        self.leaving.acquire()
        self.leaving.release()
        
def test(pid, barrier):
    while True:
        print('Process ' + str(pid) + ' started')
        barrier.barrier()
        time.sleep(random.random()*1000)
        print('Process ' + str(pid) + ' reached barrier')
        barrier.barrier()
        print('Process ' + str(pid) + ' passed barrier')
        barrier.barrier()
        
if __name__ == '__main__':
    
    numProcesses = multiprocessing.cpu_count()
    testBarrier = CyclicBarrier(numProcesses)
    processes = []
    
    for i in range(numProcesses):
        p = multiprocessing.Process(target=test, args=(i, testBarrier,))
        processes.append(p)
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()