import time
import multiprocessing

#Σε αυτήν την τροποποίηση για size = max, το μόνο που άλλαξε είναι η αφαίρεση 
#των περιττών ελέγχων counter==size, back==size και front==size
#(περιττών αφού το size είναι άπειρο)

class buffer():
    def __init__(self, size): 
        manager = multiprocessing.Manager() 
        self.contents = manager.list()
        self.size = size
        self.front = multiprocessing.Value('i', 0)
        self.back = multiprocessing.Value('i', 0)
        self.counter = multiprocessing.Value('i', -1)
        self.lock = multiprocessing.Lock()
        self.Fullcond = multiprocessing.Condition(self.lock)
        self.Emptycond = multiprocessing.Condition(self.lock)

    def myput(self, item):
        self.Fullcond.acquire()
        try:    
            self.back.value = self.back.value + 1
            self.contents.insert(self.back.value, item) 
            self.counter.value = self.counter.value + 1
          
            self.Emptycond.notify_all()
        finally:
            self.Fullcond.release()

    def myget(self):
        self.Emptycond.acquire()
        try:
            while self.counter.value == 0: 
                self.Emptycond.wait()
            
            item = self.contents[self.front.value]
            self.front.value = self.front.value + 1
            self.counter.value = self.counter.value - 1
            
            self.Fullcond.notify_all()
        finally:
            self.Emptycond.release()
        return item    

def pro(tid, mybuffer, myloop, mydelay):
    for i in range(myloop): 
        print("Prod %d item %d" % (tid,i)) 
        mybuffer.myput(i)
        time.sleep(mydelay)       
        
def con(tid, mybuffer, mydelay):
    while True: 
        i = mybuffer.myget()
        print("Cons %d item %d" % (tid,i)) 
        time.sleep(mydelay)      

if __name__ == '__main__':
    loop = 10
    npro = 2
    size = loop*npro + 1 # set buffer size to MAX
    ncon = 2
    dpro = 0.1
    dcon = 0.2
    
    a_buffer = buffer(size)
    pros = [multiprocessing.Process(target=pro, args=(i, a_buffer, loop, dpro)) for i in range(npro)]
    cons = [multiprocessing.Process(target=con, args=(i, a_buffer, dcon)) for i in range(ncon)]
    
    t1 = time.perf_counter()
    
    for t in pros:
            t.start()
    for t in cons:
            t.start()
    for t in pros:
            t.join()
    for t in cons:
            t.join()   
    
    t2 = time.perf_counter()
    print('Finished')
    print('Time to compute = {} seconds'.format(t2 - t1))  