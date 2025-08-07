import time
import threading

#Σε αυτήν την τροποποίηση για size=1 ουσιαστικά αφαίρεσα τις περιττές μεταβλητές back και front αφού ο πίνακας
#του buffer είχε μόλις ένα στοιχείο. Άρα, απλά όταν μπαίνει ένα στοιχείο στον πίνακα κλειδώνουμε τον producer
#μέχρι να αφαιρέσει το στοιχείο ο consumer

class buffer():
    def __init__(self, size): 
        self.contents = []
        self.size = size
        self.counter = 0
        self.lock = threading.Lock()
        self.Fullcond = threading.Condition(self.lock)
        self.Emptycond = threading.Condition(self.lock)

    def myput(self, item):
        self.Fullcond.acquire()
        try:
            while self.counter == 1:
                self.Fullcond.wait()
                
            self.contents.append(item) 
            self.counter = 1
          
            self.Emptycond.notify_all()
        finally:
            self.Fullcond.release()

    def myget(self):
        self.Emptycond.acquire()
        try:
            while self.counter == 0: 
                self.Emptycond.wait()
            
            item = self.contents.pop()
            self.counter = 0
            
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
    size = 1 #set buffer size to 1
    loop = 10
    npro = 2
    ncon = 2
    dpro = 0.1
    dcon = 0.2
    
    a_buffer = buffer(size)
    pros = [threading.Thread(target=pro, args=(i, a_buffer, loop, dpro)) for i in range(npro)]
    cons = [threading.Thread(target=con, args=(i, a_buffer, dcon)) for i in range(ncon)]
        
    for t in pros:
            t.start()
    for t in cons:
            t.start()
    for t in pros:
            t.join()
    for t in cons:
            t.join()   