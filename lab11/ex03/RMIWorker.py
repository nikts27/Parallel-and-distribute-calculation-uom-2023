# use Python remote object library
import Pyro5.api as pyro
import multiprocessing
import uuid

@pyro.expose
@pyro.behavior(instance_mode="single")
class WorkerInterface:
    def organize_calculation(self, start, stop):
        raise NotImplementedError("Subclasses should implement this method.")

@pyro.expose
class Worker(WorkerInterface):
    def organize_calculation(self, start, stop):
        myRange = stop - start
        step = 1.0 / myRange
        
        num_processes = multiprocessing.cpu_count()
        processes = []
        
        # Create a shared multiprocessing value representing pi
        pi_ref = multiprocessing.Value('d', 0.0)
        lock = multiprocessing.Lock()
        
        # Create processes
        for i in range(num_processes):
            p = multiprocessing.Process(target=self.calc_Pi, args=(i, myRange, num_processes, step, pi_ref, lock))
            processes.append(p)
        
        # Start processes
        for p in processes:
            p.start()
        
        # Wait for processes to finish
        for p in processes:
            p.join()
        
        return pi_ref.value * step
    
    def calc_Pi(self, blockNum, steps, num_processes, step, pi, lock):
        local_sum = 0
        
        # Calculate block range for each process
        block = steps // num_processes
        start = blockNum * block
        stop = start + block
        if blockNum == num_processes - 1:
            stop = steps

        for j in range(start, stop):
            x = (j + 0.5) * step
            local_sum += 4.0 / (1.0 + x**2)
        
        with lock:
            pi.value += local_sum

if __name__ == '__main__':
    try:
        # Get the total number of workers from the user
        number_of_workers = int(input("Give total number of workers: "))
    except ValueError:
        print("Wrong data given!")
        exit(1)
    
    # Create a Pyro daemon
    daemon = pyro.Daemon()
    ns = pyro.locate_ns()
    
    for i in range(number_of_workers):
        worker = Worker()
        uri = daemon.register(worker)
        # assign a unique name to the worker using the uuid lib
        unique_name = f"worker_{uuid.uuid4()}"
        ns.register(unique_name, uri)

    # Start the event loop of the server to wait for calls
    daemon.requestLoop()
