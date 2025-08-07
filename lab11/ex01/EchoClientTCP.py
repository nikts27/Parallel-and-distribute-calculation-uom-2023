import socket
import time

class ClientProtocol:
    
    def __init__(self):
        self.t1 = 0
        self.t2 = 0

    def prepareRequest(self):
        theResult = input("Enter math to send to server (for example: 1 + 1): ")
        self.t1 = time.perf_counter()
        return theResult

    def processReply(self,theResult):
        print("Response received from server: " + theResult)
        self.t2 = time.perf_counter()
        print('Time to compute = {} seconds'.format(self.t2 - self.t1))

class EchoClientTCP:
    HOST = "localhost"
    PORT = 1234
    serverAdd = (HOST,PORT)
    EXIT = "CLOSE"

    def main():

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect(EchoClientTCP.serverAdd)
        print("Connection to " + EchoClientTCP.HOST + " established")

        app = ClientProtocol()
        outmsg = app.prepareRequest()
        while(not(outmsg == EchoClientTCP.EXIT)):
            dataSocket.sendall(outmsg.encode())
            inmsg = dataSocket.recv(1024)
            app.processReply(inmsg.decode())
            outmsg = app.prepareRequest()
        dataSocket.sendall(outmsg.encode())

        dataSocket.close()
        print("Data Socket closed")

if __name__ == '__main__':
    EchoClientTCP.main()
