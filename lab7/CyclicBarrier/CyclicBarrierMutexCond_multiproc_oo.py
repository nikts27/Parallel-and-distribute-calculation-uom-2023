import time
import random
import multiprocessing

class CyclicBarrier():
    def __init__(self, processes):
        self.totalProcesses = processes
        self.arrived= multiprocessing.Value('i',0)
        self.waiting = multiprocessing.Value('b', False)
        self.leaving= multiprocessing.Value('b', True)
        self.l = multiprocessing.Lock()
        self.cWait = multiprocessing.Condition(self.l)
        self.cLeave = multiprocessing.Condition(self.l)
        
    def barrier(self):
        #waiting
        self.cWait.acquire()
        try:
            self.arrived.value = self.arrived.value + 1
            if self.arrived.value == self.totalProcesses:
                self.waiting.value = True
                self.leaving.value = False
            while not self.waiting.value:
                self.cWait.wait()
            self.cWait.notify_all()
        finally:
            self.cWait.release()
        
        #leaving
        self.cLeave.acquire()
        try:
            self.arrived.value = self.arrived.value - 1
            if self.arrived.value == 0:
                self.waiting.value = False
                self.leaving.value = True
            while not self.leaving.value:
                self.cLeave.wait()
            self.cLeave.notify_all()
        finally:
            self.cLeave.release()

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