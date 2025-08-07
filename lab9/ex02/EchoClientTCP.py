import socket
from Request import Request
from Reply import Reply

class ClientProtocol:

    def prepareRequest(self):
        theInput = input("Enter math to send to server (for example: 1 + 1): ")
        split_input = theInput.split()
        #create request object
        request = Request(split_input[0], split_input[2], split_input[1])
        return request

    def processReply(self, theResult):
        reply = Reply.from_string(theResult)
        print("Response received from server: " + str(reply.getResult()))

class EchoClientTCP:
    HOST = "localhost"
    PORT = 1234
    serverAdd = (HOST, PORT)
    EXIT = "CLOSE"

    @staticmethod
    def main():
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect(EchoClientTCP.serverAdd)
        print("Connection to " + EchoClientTCP.HOST + " established")

        app = ClientProtocol()
        outmsg = app.prepareRequest()
        while not (str(outmsg) == EchoClientTCP.EXIT):
            dataSocket.sendall(str(outmsg).encode())
            inmsg = dataSocket.recv(1024).decode()
            app.processReply(inmsg)
            outmsg = app.prepareRequest()
        dataSocket.sendall(EchoClientTCP.EXIT.encode())

        dataSocket.close()
        print("Data Socket closed")

if __name__ == '__main__':
    EchoClientTCP.main()