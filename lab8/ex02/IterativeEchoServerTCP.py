import socket

class ServerProtocol:

    def processRequest(self,theInput):
        math = theInput.split()
        
        #check for correct data
        if len(math) != 3:
            theOutput = 'Not right data given from client. Try again'
        else:
            theOutput = self.compute_math(math)
        print("Send result to client: " + str(theOutput))
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


class IterativeEchoServerTCP:
    #Server address
    PORT = 1234
    serverAdd = ("localhost",PORT)
    EXIT = "CLOSE"

    def main():
        connectionSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connectionSocket.bind(IterativeEchoServerTCP.serverAdd)
        connectionSocket.listen(10)

        while True:
            print("Server is listening to port: " + str(IterativeEchoServerTCP.PORT))

            conn, add = connectionSocket.accept()
            print("Received request from " + str(add))

            inmsg = conn.recv(1024)

            app = ServerProtocol()
            outmsg = app.processRequest(inmsg.decode())
            while(not(outmsg == IterativeEchoServerTCP.EXIT)):
                conn.sendall(outmsg.encode())
                inmsg = conn.recv(1024)
                outmsg = app.processRequest(inmsg.decode())

        conn.close()
        print("Data socket closed")

if __name__ == '__main__':
    IterativeEchoServerTCP.main()
