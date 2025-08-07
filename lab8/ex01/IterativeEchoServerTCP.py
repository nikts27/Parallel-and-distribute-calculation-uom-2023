import socket

class ServerProtocol:

    def processRequest(self,theInput):
        print("Received message from client: " + theInput)
        #split the input to get the command number and offset
        split_input = theInput.split()
        #get the response according to the command
        if split_input[-2] == '1':
            theOutput = theInput[:-3].lower()
        elif split_input[-2] == '2':
            theOutput = theInput[:-3].upper()
        elif split_input[-2] == '3':
            theOutput = self.encryptMessage(split_input[:-2], split_input[-1])
        elif split_input[-2] == '4':
            theOutput = self.decryptMessage(split_input[:-2], split_input[-1])
        else:
            theOutput = theInput
            print("No command given. Send the message back")
        print("Send message to client: " + theOutput)
        return theOutput
    
    def encryptMessage(self, message, offset):
        result = ""
        for word in message:
            for character in word:
                original_alphabet_position = ord(character) - ord('a')
                new_alphabet_position = (original_alphabet_position + int(offset)) % 26
                new_character = chr(ord('a') + new_alphabet_position)
                result += new_character
            result += " "
        return result
    
    def decryptMessage(self, message, offset):
        result = ""
        for word in message:
            for character in word:
                original_alphabet_position = ord(character) - ord('a')
                new_alphabet_position = (original_alphabet_position - int(offset)) % 26
                new_character = chr(ord('a') + new_alphabet_position)
                result += new_character
            result += " "
        return result 


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
