import socket
import multiprocessing
 
# Handle the computation of Pi for a given range of steps.
class WorkerProtocol():
    
    def compute(self, theInput):
        split_input = theInput.split()
        myStart = int(split_input[0])
        myStop = int(split_input[1])
        id = int(split_input[2])
        myRange = myStop - myStart
        step = 1.0 / myRange
        
        print(f"Worker {id} calculates range {myRange}")
        num_processes = multiprocessing.cpu_count()
        processes = []
        
        # Create a shared multiprocessing value representing pi
        pi_ref = multiprocessing.Value('d', 0.0)
        lock = multiprocessing.Lock()
        
        # Create processes
        for i in range(num_processes):
            p = multiprocessing.Process(target=self.calc_Pi, args=(i, myRange, num_processes, step, pi_ref, lock,))
            processes.append(p)
        
        # Start processes
        for p in processes:
            p.start()
        
        # Wait for processes to finish
        for p in processes:
            p.join()
        
        pi = pi_ref.value * step
        
        print(f"Worker {id}, Result: {pi}")
        return str(pi)
        
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

class NumIntWorkerTCP():
    HOST = "localhost"
    PORT = 1234
    serverAdd = (HOST, PORT)
    
    @staticmethod
    def main():
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect(NumIntWorkerTCP.serverAdd)
        
        app = WorkerProtocol()
        inmsg = dataSocket.recv(1024).decode()
        outmsg = app.compute(inmsg)
        dataSocket.sendall(outmsg.encode())
        dataSocket.close()

if __name__ == '__main__':
    NumIntWorkerTCP.main()
