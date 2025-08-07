import socket
import threading

class ServerProtocol:
    
    def __init__(self, cnum):
        self.client = cnum

    def processRequest(self,theInput):
        math = theInput.split()
        
        #check for correct data
        if len(math) != 3:
            theOutput = 'Not right data given from client. Try again'
        else:
            theOutput = self.compute_math(math)
        print("Send result to client " + str(self.client) + ": " + str(theOutput))
        return str(theOutput)
    
    #get the result
    def compute_math(self, math):
        #get the numbers and the operator
        try:
            a = float(math[0])
            b = float(math[2])
        except ValueError:
            return 'Not right data given from client. Try again'
        opp = math[1]
                
        #perform the right calculation according to the operator
        if opp == '+':
            theOutput = a+b
        elif opp == '-':
            theOutput = a-b
        elif opp == '*':
            theOutput = a*b
        elif opp == '/' and b != 0: #division with zero doesn't exist
            theOutput = a/b
        else:
            return 'Not right data given from client. Try again'
        return theOutput

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
    EXIT = "CLOSE"

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