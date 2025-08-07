import socket
import threading
import multiprocessing
from Pi import PiCalc

class ServerProtocol:
    
    def __init__(self, cnum, shared_dict):
        self.client = cnum
        self.dictionary = shared_dict
        self.lock = multiprocessing.Lock()

    def processRequest(self,theInput):
        #check for correct data       
        try:
           theInput = int(theInput)
        except ValueError as e:
           print('Integer convertion error: {}' .format(e))
           exit(1)
        
        #check if pi for the given number of steps is already calculated else calculate it
        if self.checkIfCalculated(theInput) != -1:
            pi = self.checkIfCalculated(theInput)
        else:
            pi = self.calcPi(theInput)
            
        print('Pi calculated with ' + str(theInput) + ' steps (from client ' + str(self.client) + '): ' + str(pi))
        return str(pi)
    
    def checkIfCalculated(self, numberOfSteps):
        with self.lock:
            #check if we calculate for the given number of steps in the dictionary.
            #If yes, return the value. If no, return -1
            for key, value in self.dictionary.items():
                if key==numberOfSteps:
                   return value
        return -1
    
    #calculate pi value with the given number of steps, parallel
    def calcPi(self, numberOfSteps):
        # Get the number of CPU cores
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
        
      
class ServerThread(threading.Thread):
    
    
    def __init__(self, conn, cnum, shared_dict):
        super(ServerThread, self).__init__()
        self.dataConn = conn
        self.client = cnum
        self.dictionary = shared_dict
    
    def run(self):
        inmsg = self.dataConn.recv(1024)

        try:
            app = ServerProtocol(self.client ,self.dictionary)
            outmsg = app.processRequest(inmsg.decode())
            while(not(outmsg == MultithreadedEchoServerTCP.EXIT)):
                self.dataConn.sendall(outmsg.encode())
                inmsg = self.dataConn.recv(1024)
                outmsg = app.processRequest(inmsg.decode())
        
            self.dataConn.close()
            print("Data socket closed")
        except IOError:
            print("I/O Error!")


class MultithreadedEchoServerTCP:
    #Server address
    PORT = 1234
    serverAdd = ("localhost",PORT)
    EXIT = "EXIT"

    def main():
        connectionSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connectionSocket.bind(MultithreadedEchoServerTCP.serverAdd)
        connectionSocket.listen(10)
        
        #counter of different clients in the server
        count = 1

        while True:
            print("Server is listening to port: " + str(MultithreadedEchoServerTCP.PORT))

            conn, add = connectionSocket.accept()
            print("Received request from " + str(add))
            
            #create a shared dictionary across clients and processes
            shared_dict = multiprocessing.Manager().dict()

            sthread = ServerThread(conn, count, shared_dict)
            sthread.start()
            
            count += 1

if __name__ == '__main__':
    MultithreadedEchoServerTCP.main()