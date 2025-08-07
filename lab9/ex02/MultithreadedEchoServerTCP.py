import socket
import threading
from Request import Request
from Reply import Reply

class ServerProtocol:
    
    def __init__(self, cnum):
        self.client = cnum

    def processRequest(self, theInput):
        try:
            request = Request.from_string(theInput)
            theOutput = self.compute_math(request)
            print("Send result to client " + str(self.client) + ": " + str(theOutput.getResult()))
            return theOutput
        except Exception as e:
            print(f"Error processing request: {e}")
            return Reply("Error")

    #get the result
    def compute_math(self, math):
        theOutput = Reply(0)
        
        #get the numbers and the operator
        try:
            a = float(math.getFirstNumber())
            b = float(math.getSecondNumber())
            opp = math.getOperator()
        except ValueError:
            theOutput.setResult('Invalid data type')

        #perform the right calculation according to the operator
        if opp == '+':
            theOutput.setResult(a + b)
        elif opp == '-':
            theOutput.setResult(a - b)
        elif opp == '*':
            theOutput.setResult(a * b)
        elif opp == '/' and b != 0: #division with zero doesn't exist
            theOutput.setResult(a / b)
        else:
            theOutput.setResult('Invalid operation')
        return theOutput

#create server thread class to handle multiple clients    
class ServerThread(threading.Thread):

    def __init__(self, conn, cnum):
        super(ServerThread, self).__init__()
        self.dataConn = conn
        self.client = cnum

    def run(self):
        try:
            app = ServerProtocol(self.client)
            while True:
                inmsg = self.dataConn.recv(1024).decode()
                if not inmsg:
                    break
                if inmsg == MultithreadedEchoServerTCP.EXIT:
                    break
                outmsg = app.processRequest(inmsg)
                self.dataConn.sendall(str(outmsg).encode())

            self.dataConn.close()
        except IOError as e:
            print(f"I/O Error: {e}")

class MultithreadedEchoServerTCP:
    PORT = 1234
    serverAdd = ("localhost", PORT)
    EXIT = "CLOSE"

    @staticmethod
    def main():
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.bind(MultithreadedEchoServerTCP.serverAdd)
        connectionSocket.listen(10)
        
        #counter of different clients in the server
        count = 1

        while True:
            print(f"Server is listening on port: {MultithreadedEchoServerTCP.PORT}")

            conn, addr = connectionSocket.accept()
            print(f"Received request from {addr}")

            #create new thread for every client sending requests
            sthread = ServerThread(conn, count)
            sthread.start()
            
            count += 1

if __name__ == '__main__':
    MultithreadedEchoServerTCP.main()