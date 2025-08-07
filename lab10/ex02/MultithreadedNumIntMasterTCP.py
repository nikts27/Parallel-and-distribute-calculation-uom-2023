import socket
import threading
from Pi import Pi

class MasterProtocol():
    
    def __init__(self, wnum, start, stop, pi_value, lock):
        self.id = wnum
        self.myStart = start
        self.myStop = stop
        self.pi = pi_value
        self.lock = lock
    
    def prepareRequest(self):
        return str(self.myStart) + " " + str(self.myStop) + " " + str(self.id)
    
    def processReply(self, theInput):
        with self.lock:
            self.pi.addTo(float(theInput)) 

# thread class responsible for communication with a single worker.
class MasterThread(threading.Thread):
    
    def __init__(self, dataSocket, wnum, start, stop, pi_value, lock):
        super(MasterThread, self).__init__()
        self.conn = dataSocket
        self.id = wnum
        self.myStart = start
        self.myStop = stop
        self.pi = pi_value
        self.lock = lock
        
    def run(self):
        try:
            app = MasterProtocol(self.id, self.myStart, self.myStop, self.pi, self.lock)
            outmsg = app.prepareRequest()
            self.conn.sendall(outmsg.encode())
            inmsg = self.conn.recv(1024).decode()
            app.processReply(inmsg)
        except IOError:
            print(f"Master Thread {self.id}: I/O error!")
        except Exception as e:
            print(f"Master Thread {self.id}: {str(e)}")
        finally:
            self.conn.close()

class MultithreadedNumIntMasterTCP():
    PORT = 1234
    serverAdd = ("localhost", PORT)
    
    @staticmethod
    def main():
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.bind(MultithreadedNumIntMasterTCP.serverAdd)
        connectionSocket.listen(10)
        
        try:
            # Get the number of workers and total calculation steps from the user
            num_workers = int(input("Give number of workers: "))
            number_of_steps = int(input("Give total number of calculation steps: "))
        except ValueError:
            print("Wrong data given!")
            return
        
        mThreads = []
        pi_value = Pi() # Shared Pi object for result aggregation
        lock = threading.Lock() # Lock to synchronize access to shared Pi object
        
        # Divide the calculation work among the workers
        block = number_of_steps // num_workers
        for i in range(num_workers):
            start = i * block
            stop = start + block
            if i == num_workers - 1:
                stop = number_of_steps
            conn, addr = connectionSocket.accept()
            t = MasterThread(conn, i, start, stop, pi_value, lock)
            mThreads.append(t)
        
        # start master threads
        for t in mThreads:
            t.start()
        print("All started")
        
        # wait for threads to finish
        for t in mThreads:
            t.join()
        pi_value.printResult()

if __name__ == '__main__':
    MultithreadedNumIntMasterTCP.main()
