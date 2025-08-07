import threading
import multiprocessing

class DoubleCounter:
    def __init__(self):
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.n1 = 0
        self.n2 = 0

    def increment_n1(self):
        with self.lock1:
            self.n1 += 1
            print("n1: " + str(self.n1))

    def increment_n2(self):
        with self.lock2:
            self.n2 += 1
            print("n2: " + str(self.n2))

# Test the DoubleCounter class with multiple threads
def test_counter(counter, num_iterations):
    for i in range(num_iterations):
        counter.increment_n1()
        counter.increment_n2()

if __name__ == "__main__":
    
    num_threads = multiprocessing.cpu_count()
    num_iterations = 1000
    counter = DoubleCounter()
    threads = []

    # Create threads
    for i in range(num_threads):
        t = threading.Thread(target=test_counter, args=(counter, num_iterations))
        threads.append(t)
    
    # Start threads
    for t in threads:
        t.start()
    
    # Wait for threads to finish
    for t in threads:
        t.join()