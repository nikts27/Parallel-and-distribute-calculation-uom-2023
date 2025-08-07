import Pyro5.api as pyro
import multiprocessing
from Pi import PiCalc

@pyro.expose
class RemoteObject:
    
    def __init__(self):
        self.dictionary = multiprocessing.Manager().dict() 
        self.lock = multiprocessing.Lock()
    
    def calc_Pi(self, steps):
        #check for correct data
        try:
           numberOfSteps = int(steps)
        except ValueError as e:
           print('Integer convertion error: {}' .format(e))
           exit(1)
        
        #check if we already calculated for the given number of steps
        if self.checkIfCalculated(numberOfSteps) != -1:
            return self.checkIfCalculated(numberOfSteps)
           
        #Get the number of CPU cores
        num_processes = multiprocessing.cpu_count()
        processes = []
        
        #create a shared multiprocessing value representing pi
        pi_ref = multiprocessing.Value('d', 0.0)
        
        #create processes
        for i in range(num_processes):
            processes.append(PiCalc(i, numberOfSteps, pi_ref))
        
        #start processes
        for p in processes:
            p.start()
        
        #wait for processes to finish
        for p in processes:
            p.join()
            
        pi = pi_ref.value * (1.0/numberOfSteps)
        
        #add to dictionary
        with self.lock:
            self.dictionary[numberOfSteps] = pi
        
        return pi
    
    def checkIfCalculated(self, steps):
        with self.lock:
            #check if we calculate for the given number of steps in the dictionary.
            #If yes, return the value. If no, return -1
            for key, value in self.dictionary.items():
                if key==steps:
                   return value
        return -1

if __name__ == '__main__':
    # Create a Pyro daemon
    daemon = pyro.Daemon()

    # Register the remote object with a name
    uri = daemon.register(RemoteObject)
    
    # Register the object with the name server
    ns = pyro.locate_ns()  # locate the name server
    ns.register("example.remoteobject", uri)  # register the object with a name
    
    # Start the event loop of the server to wait for calls
    daemon.requestLoop()