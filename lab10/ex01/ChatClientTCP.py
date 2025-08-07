import socket
import threading
from queue import Queue, Empty

class ClientProtocol:
    def sendMessage(self):
        return input("Send message, CLOSE for exit: ")

    def receiveMessage(self, theInput):
        print("\nReceived message: " + theInput)
        return input("Send a reply, CLOSE for exit: ")

class SendThread(threading.Thread):
    def __init__(self, conn, message_queue, stop_event, semaphore, typing_lock):
        super(SendThread, self).__init__()
        self.dataConn = conn
        self.message_queue = message_queue
        self.stop_event = stop_event
        self.semaphore = semaphore
        self.typing_lock = typing_lock

    def run(self):
        try:
            app = ClientProtocol()
            while not self.stop_event.is_set():
                with self.typing_lock:
                    # Get the initial message from user input
                    outmsg = app.sendMessage() or ""  # Ensure outmsg is a string
                self.dataConn.sendall(outmsg.encode())
                if outmsg == ChatClientTCP.EXIT:
                    self.stop_event.set()
                    return

                # Wait for replies from the receive thread
                while not self.stop_event.is_set():
                    self.semaphore.acquire()  # Wait for the semaphore to be released by the ReceiveThread
                    try:
                        outmsg = self.message_queue.get(timeout=1) or ""  # Ensure outmsg is a string
                        outmsg_split = outmsg.split()
                        self.dataConn.sendall(outmsg.encode())
                        if outmsg_split == ChatClientTCP.EXIT:
                            self.stop_event.set()
                            break
                    except Empty:
                        continue
        except IOError:
            print('SendThread: I/O Error!')
        except Exception as e:
            print(f"SendThread Error: {e}")
        finally:
            self.dataConn.close()

class ReceiveThread(threading.Thread):
    def __init__(self, conn, message_queue, stop_event, semaphore, typing_lock):
        super(ReceiveThread, self).__init__()
        self.dataConn = conn
        self.message_queue = message_queue
        self.stop_event = stop_event
        self.semaphore = semaphore
        self.typing_lock = typing_lock

    def run(self):
        try:
            app = ClientProtocol()
            while not self.stop_event.is_set():
                inmsg = self.dataConn.recv(1024).decode()
                inmsg_split = inmsg.split()
                if inmsg_split == ChatClientTCP.EXIT:
                    self.stop_event.set()
                    break
                with self.typing_lock:
                    reply = app.receiveMessage(inmsg)  # Handle the received message and get a reply
                split_reply = reply.split()
                if split_reply == ChatClientTCP.EXIT:
                    self.stop_event.set()
                    break
                self.message_queue.put(reply)  # Put the reply in the message queue
                self.semaphore.release()  # Notify the SendThread
        except IOError:
            print('ReceiveThread: I/O Error!')
        except Exception as e:
            print(f"ReceiveThread Error: {e}")
        finally:
            self.dataConn.close()

def register(socket):
    initial_message = socket.recv(1024).decode()
    print(initial_message)
    if "Please provide an ID:" in initial_message:
        client_id = input("Enter your ID: ")
        socket.sendall(client_id.encode())
        confirmation_message = socket.recv(1024).decode()
        print(confirmation_message)

class ChatClientTCP:
    HOST = "localhost"
    PORT = 1234
    serverAdd = (HOST, PORT)
    EXIT = "CLOSE"

    @staticmethod
    def main():
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect(ChatClientTCP.serverAdd)
        print("Connection to " + ChatClientTCP.HOST + " established")

        # Initial ID registration or welcome back message
        register(dataSocket)

        stop_event = threading.Event()  # Event to signal stopping the threads
        message_queue = Queue()  # Queue for messages
        response_mux = threading.Semaphore(0)  # Semaphore for synchronizing messages
        typing_lock = threading.Lock()  # Lock to signal when the user is typing

        # Thread that has the task to send messages to the server
        send_thread = SendThread(dataSocket, message_queue, stop_event, response_mux, typing_lock)
        # Thread that has the task to receive and print messages the server returns to the client
        receive_thread = ReceiveThread(dataSocket, message_queue, stop_event, response_mux, typing_lock)

        send_thread.start()
        receive_thread.start()

if __name__ == '__main__':
    ChatClientTCP.main()