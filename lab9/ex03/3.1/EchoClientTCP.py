import socket

class ClientProtocol:

    def prepareRequest(self):
        #give number of steps
        theInput = input("Enter number of steps of pi calculation (select -1 to finish): ")
        return theInput

    def processReply(self,theResult):
        print("Response received from server: " + theResult)

class EchoClientTCP:
    HOST = "localhost"
    PORT = 1234
    serverAdd = (HOST,PORT)
    EXIT = "-1"

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
