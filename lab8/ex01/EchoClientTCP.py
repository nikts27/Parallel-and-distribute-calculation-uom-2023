import socket
from spellchecker import SpellChecker

class ClientProtocol:

    def prepareRequest(self):
        print("Command 1: Turn capital letters to small")
        print("Command 2: Turn small letters to capital")
        print("Command 3: Encrypt the message")
        print("Command 4: Decrypt the message")
        theOutput = input("Enter message to send to server, plus command (1,2,3 or 4) and " +
                          "offset (if you choose command 1 or 2 give offset 0), for example 'Hello 3 43' or 'Hello 2 0': ")
        split_output = theOutput.split()
        #if command=4, don't check for spelling mistakes
        if (split_output[-2] == '4'):
            return theOutput
        #check for spelling mistakes in the string
        corrected_output = self.check_message_spelling(split_output[:-2])
        corrected_output += " " + split_output[-2] + " " + split_output[-1]
        return corrected_output

    def processReply(self,theInput):
        print("Message received from server: " + theInput)
    
    #correct the message's spelling
    def check_message_spelling(self, message):
        spell = SpellChecker()
        result = ""

        for word in message:
            result += spell.correction(word) + " "
        return result
        
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
