import time
import random
import threading
import multiprocessing

class CyclicBarrier():
    def __init__(self, threads):
        self.totalThreads = threads
        self.arrived = 0
        self.waiting = False
        self.leaving= True
        self.l = threading.Lock()
        self.cWait = threading.Condition(self.l)
        self.cLeave = threading.Condition(self.l)
        
    def barrier(self):
        #waiting
        self.cWait.acquire()
        try:
            self.arrived += 1
            if self.arrived == self.totalThreads:
                self.waiting = True
                self.leaving = False
            while not self.waiting:
                self.cWait.wait()
            self.cWait.notify_all()
        finally:
            self.cWait.release()
        
        #leaving
        self.cLeave.acquire()
        try:
            self.arrived -= 1
            if self.arrived == 0:
                self.waiting = False
                self.leaving = True
            while not self.leaving:
                self.cLeave.wait()
            self.cLeave.notify_all()
        finally:
            self.cLeave.release()

def test(tid, barrier):
    while True:
        print('Thread ' + str(tid) + ' started')
        barrier.barrier()
        time.sleep(random.random()*1000)
        print('Thread ' + str(tid) + ' reached barrier')
        barrier.barrier()
        print('Thread ' + str(tid) + ' passed barrier')
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