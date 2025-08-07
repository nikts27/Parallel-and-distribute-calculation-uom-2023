import time
import multiprocessing

# Σε αυτήν την έκδοση για Ν producers και 1 consumer, το μόνο που άλλαξε είναι η εισαγωγή μιας μεταβλητής item
# τύπου Multiprocessing.Value και η οποία χρησιμοποιείται για την διατήρηση της τιμής που αυξάνουν οι 
# producers και καταναλώνει έπειτα ο consumer. Για την βεβαιότητα της απρόσκοπτης μεταβολής της κάθε φορά που 
# εκτελείται η pro, εισαγάγαμε και μια μεταβλητή lock για να δημιουργήσουμε αμοιβαίο αποκλεισμό
# Η κλάση buffer παραμένει ως έχει

class buffer():
    def __init__(self, size): 
        manager = multiprocessing.Manager() 
        self.contents = manager.list()
        self.size = size
        self.front = multiprocessing.Value('i', 0)
        self.back = multiprocessing.Value('i', size - 1)
        self.counter = multiprocessing.Value('i', 0)
        self.lock = multiprocessing.Lock()
        self.Fullcond = multiprocessing.Condition(self.lock)
        self.Emptycond = multiprocessing.Condition(self.lock)

    def myput(self, item):
        self.Fullcond.acquire()
        try:
            while self.counter.value == self.size: 
                self.Fullcond.wait()
                
            self.back.value = self.back.value + 1
            if self.back.value == self.size : self.back.value = 0 
            self.contents.insert(self.back.value, item.value) 
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
            if self.front.value == self.size : self.front.value = 0 
            self.counter.value = self.counter.value - 1
            
            self.Fullcond.notify_all()
        finally:
            self.Emptycond.release()
        return item    

def pro(tid, mybuffer, myloop, mydelay, item, lock):
    for i in range(myloop): 
        time.sleep(mydelay) 
        with lock: 
            item.value += 1
            print("Prod %d item %d" % (tid, item.value)) 
            mybuffer.myput(item)    
        
def con(tid, mybuffer, mydelay):
    while True: 
        i = mybuffer.myget()
        print("Cons %d item %d" % (tid,i)) 
        time.sleep(mydelay)            

if __name__ == '__main__':
    size = 20
    loop = 10
    npro = 2
    ncon = 1 #set number of consumers to 1
    dpro = 0.1
    dcon = 0.2
    
    item = multiprocessing.Value('i', -1)
    item_lock = multiprocessing.Lock()
    
    a_buffer = buffer(size)
    pros = [multiprocessing.Process(target=pro, args=(i, a_buffer, loop, dpro, item, item_lock)) for i in range(npro)]
    cons = [multiprocessing.Process(target=con, args=(i, a_buffer, dcon)) for i in range(ncon)]
        
    for t in pros:
            t.start()
    for t in cons:
            t.start()
    for t in pros:
            t.join()
    for t in cons:
            t.join()   