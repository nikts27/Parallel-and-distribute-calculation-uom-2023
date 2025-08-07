from threading import Thread
from abc import ABC, abstractmethod

#abstract base class for custom threads
class AbstractThread(Thread, ABC):
    
    @abstractmethod
    def __init__(self, num):
        super(AbstractThread, self).__init__()
        self.num = num
        
    @abstractmethod
    def run(self):
        pass
    
class MyThread1(AbstractThread):
    
    def __init__(self, num):
        super(MyThread1, self).__init__(num)
    
    def run(self):
        print("Hello from thread of class: " + str(self.num))
        print("Thread from class " + str(self.num) + " finished")
        
class MyThread2(AbstractThread):
    
    def __init__(self, num):
        super(MyThread2, self).__init__(num)
    
    def run(self):
        print("Hello from thread of class: " + str(self.num))
        print("Thread from class " + str(self.num) + " finished")


if __name__ == '__main__':
    
    threads = []
    
    print('Opening threads from 2 different classes')
    
    #create threads
    threads.append(MyThread1(1))
    threads.append(MyThread2(2))
    
    #run the threads
    for t in threads:
        t.start()
    
    #wait for threads to finish
    for t in threads:
        t.join()
    
    print('Finished')