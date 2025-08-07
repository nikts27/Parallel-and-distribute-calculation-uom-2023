import socket
import threading
import multiprocessing
from Pi import PiCalc

class ServerProtocol:
    
    def __init__(self, cnum):
        self.client = cnum

    def processRequest(self,theInput):
        #check for correct data
        try:
           theInput = int(theInput)
        except ValueError as e:
           print('Integer convertion error: {}' .format(e))
           exit(1)
        
        #calculate and return pi value
        pi = self.calcPi(theInput)
        print('Pi calculated with ' + str(theInput) + "steps (from client " + str(self.client) + "):" + str(pi))
        return str(pi)
    
    #calculate pi value with the given number of steps, parallel
    def calcPi(self, numberOfSteps):
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
        
        return pi_ref.value * (1.0/numberOfSteps)        
        
#create server thread class to handle multiple clients      
class ServerThread(threading.Thread):
    
    def __init__(self, conn, cnum):
        super(ServerThread, self).__init__()
        self.dataConn = conn
        self.client = cnum
    
    def run(self):
        inmsg = self.dataConn.recv(1024)

        try:
            app = ServerProtocol(self.client)
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

            #create new thread for every client sending requests
            sthread = ServerThread(conn, count)
            sthread.start()
            
            count += 1

if __name__ == '__main__':
    MultithreadedEchoServerTCP.main()