import time
import multiprocessing

# Σε αυτήν την έκδοση για size=1 αφαίρεσα τις περιττές μεταβλητές back και front αφού ο πίνακας
# του buffer είχε μόλις ένα στοιχείο. Επίσης, αφαίρεσα τον σηματοφορέα mux αφού δεν χρειάζεται να υπάρχει
# αμοιβαίος αποκλεισμός για το buffer. Κράτησα τους σηματοφορείς toPut και toGet ομως, για να εξασφαλίζω αυστηρή εναλλαγή
# παραγωγού-καταναλωτή.

class buffer():
    def __init__(self, size): 
        manager = multiprocessing.Manager() 
        self.contents = manager.list()
        self.size = size
        self.toPut = multiprocessing.Semaphore(self.size)
        self.toGet = multiprocessing.Semaphore(0)
        
    def myput(self, item):
        self.toPut.acquire()
            
        self.contents.append(item)
                 
        self.toGet.release()

    def myget(self):
        self.toGet.acquire()
            
        item = self.contents.pop()
                    
        self.toPut.release()
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
    size = 1 #set buffer size to 1
    loop = 10
    npro = 2
    ncon = 2
    dpro = 0.1
    dcon = 0.2
    
    a_buffer = buffer(size)
    pros = [multiprocessing.Process(target=pro, args=(i, a_buffer, loop, dpro)) for i in range(npro)]
    cons = [multiprocessing.Process(target=con, args=(i, a_buffer, dcon)) for i in range(ncon)]
        
    for t in pros:
            t.start()
    for t in cons:
            t.start()
    for t in pros:
            t.join()
    for t in cons:
            t.join()    