from threading import Thread
from abc import ABC, abstractmethod

#abstract base class for custom threads
class AbstractThread(Thread, ABC):
    
    @abstractmethod
    def __init__(self, t_num, c_num):
        super(AbstractThread, self).__init__()
        self.t_num = t_num
        self.c_num = c_num
                
    @abstractmethod
    def run(self):
        pass
    
class MyThread1(AbstractThread):
    
    def __init__(self, t_num, c_num):
        super(MyThread1, self).__init__(t_num, c_num)
    
    def run(self):
        print("Hello from thread: " + str(self.t_num) + " of class: " + str(self.c_num))
        print("Thread: " + str(self.t_num) + " from class " + str(self.c_num) + " finished")
        
class MyThread2(AbstractThread):
    
    def __init__(self, t_num, c_num):
        super(MyThread2, self).__init__(t_num, c_num)
    
    def run(self):
        print("Hello from thread: " + str(self.t_num) + " of class: " + str(self.c_num))
        print("Thread: " + str(self.t_num) + " from class " + str(self.c_num) + " finished")


if __name__ == '__main__':
    
    threads = []
    
    print('Opening various threads from 2 different classes')
    
    #create threads
    for i in range(5):
        threads.append(MyThread1(i+1, 1))
        threads.append(MyThread2(i+1, 2))
    
    #run the threads
    for t in threads:
        t.start()
    
    #wait for threads to finish
    for t in threads:
        t.join()
    
    print('Finished')