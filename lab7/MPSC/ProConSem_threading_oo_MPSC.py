import time
import threading

# Σε αυτήν την έκδοση για N producer και 1 consumer, η μόνη αλλαγή που έγινε στην κλάση buffer είναι η αφαίρεση του αμοιβαίου
# αποκλεισμού για τις μεταβλητές front, back. Άρα, ουσιαστικά ο σηματοφορέας mux ελέγχει μόνο την ενημέρωση
# της λίστας contents. Επίσης, εισαγάγαμε μια μεταβλητή item τύπου λίστας 
# και η οποία χρησιμοποιείται για την διατήρηση της τιμής που αυξάνουν οι 
# producers και καταναλώνει έπειτα ο consumer (αυτό γίνεται στην θέση item[0]). 
# Για την βεβαιότητα της απρόσκοπτης μεταβολής της κάθε φορά που 
# εκτελείται η pro, εισαγάγαμε και μια μεταβλητή lock για να δημιουργήσουμε αμοιβαίο αποκλεισμό
# Η κλάση buffer παραμένει ως έχει

class buffer():
    def __init__(self, size): 
        self.contents = []
        self.size = size
        self.front = 0
        self.back = size -1
        self.mux = threading.Semaphore(1)
        self.toPut = threading.Semaphore(self.size)
        self.toGet = threading.Semaphore(0)
        
    def myput(self, item):
        self.toPut.acquire()
        self.back += 1
        if self.back == self.size : self.back = 0 
            
        self.mux.acquire()
        self.contents.insert(self.back, item[0]) 
        self.mux.release()
        
        self.toGet.release()

    def myget(self):
        self.toGet.acquire()
        
        self.mux.acquire()    
        item = self.contents[self.front]
        self.mux.release()
        
        self.front += 1
        if self.front == self.size : self.front = 0 
                    
        self.toPut.release()
        return item  

def pro(tid, mybuffer, myloop, mydelay, item, lock):
    for i in range(myloop): 
        time.sleep(mydelay) 
        with lock: 
            item[0] += 1
            print("Prod %d item %d" % (tid, item[0])) 
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
    
    item = []
    item.append(-1)
    item_lock = threading.Lock()
    
    a_buffer = buffer(size)
    pros = [threading.Thread(target=pro, args=(i, a_buffer, loop, dpro, item, item_lock)) for i in range(npro)]
    cons = [threading.Thread(target=con, args=(i, a_buffer, dcon)) for i in range(ncon)]
        
    for t in pros:
            t.start()
    for t in cons:
            t.start()
    for t in pros:
            t.join()
    for t in cons:
            t.join()   