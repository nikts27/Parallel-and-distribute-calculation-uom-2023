import time
import multiprocessing

# Σε αυτήν την έκδοση για N producer και 1 consumer, η μόνη αλλαγή που έγινε στην κλάση buffer είναι η αφαίρεση του αμοιβαίου
# αποκλεισμού για τις μεταβλητές front, back. Άρα, ουσιαστικά ο σηματοφορέας mux ελέγχει μόνο την ενημέρωση
# της λίστας contents. Επίσης, εισαγάγαμε μια μεταβλητή item τύπου Multiprocessing.Value 
# και η οποία χρησιμοποιείται για την διατήρηση της τιμής που αυξάνουν οι 
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
        self.mux = multiprocessing.Semaphore(1)
        self.toPut = multiprocessing.Semaphore(self.size)
        self.toGet = multiprocessing.Semaphore(0)
        
    def myput(self, item):
        self.toPut.acquire()
        self.back.value += 1
        if self.back.value == self.size : self.back.value = 0 
            
        self.mux.acquire()
        self.contents.insert(self.back.value, item.value) 
        self.mux.release()
        
        self.toGet.release()

    def myget(self):
        self.toGet.acquire()
        
        self.mux.acquire()    
        item = self.contents[self.front.value]
        self.mux.release()
        
        self.front.value += 1
        if self.front.value == self.size : self.front.value = 0 
                    
        self.toPut.release()
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