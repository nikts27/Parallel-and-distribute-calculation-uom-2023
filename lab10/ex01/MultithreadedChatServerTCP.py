import socket
import threading

class ServerProtocol:
    def __init__(self, conn, cnum):
        self.id = cnum
        self.conn = conn

    def getClientID(self, db, address, lock):
        with lock:
            if address in db:
                self.id = db[address]
                self.conn.sendall(f"Welcome back, client {self.id}".encode())
            else:
                self.conn.sendall("Please provide an ID:".encode())
                self.id = self.conn.recv(1024).decode().strip()
                db[address] = self.id
                self.conn.sendall(f"Thank you! Your ID {self.id} is registered.".encode())

    def processRequest(self, theInput):
        print(f"Received message from client {self.id}: {theInput}")
        theOutput = theInput + " from client " + self.id
        print(f"Send message to clients: {theOutput}")
        return theOutput

class ServerThread(threading.Thread):
    def __init__(self, conn, addr, client_db, clients, lock, clients_lock):
        super(ServerThread, self).__init__()
        self.conn = conn
        self.addr = addr
        self.client_db = client_db
        self.clients = clients
        self.lock = lock
        self.clients_lock = clients_lock
        self.id = ""

    def run(self):
        try:
            app = ServerProtocol(self.conn, self.id)
            app.getClientID(self.client_db, self.addr, self.lock)
            
            # Add the new connection to the list of active clients
            with self.clients_lock:
                self.clients[self.addr] = self.conn

            while True:
                inmsg = self.conn.recv(1024)
                if not inmsg:
                    break
                inmsg_decoded = inmsg.decode()
                outmsg = app.processRequest(inmsg_decoded)
                
                # Broadcast the message to all clients except the sender
                with self.clients_lock:
                    for client_addr, client_conn in self.clients.items():
                        if client_addr != self.addr:
                            try:
                                client_conn.sendall(outmsg.encode())
                            except Exception as e:
                                print(f"Error sending to {client_addr}: {e}")
                        
                if inmsg_decoded == MultithreadedChatServerTCP.EXIT:
                    break
        except IOError:
            print('ServerThread: I/O Error!')
        except Exception as e:
            print(f"ServerThread Error: {e}")
        finally:
            self.conn.close()
            print(f"Connection with client {self.id} closed")
            # Remove the connection from the list of clients
            with self.clients_lock:
                if self.addr in self.clients:
                    del self.clients[self.addr]

class MultithreadedChatServerTCP:
    PORT = 1234
    serverAdd = ("localhost", PORT)
    EXIT = "CLOSE"

    @staticmethod
    def main():
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.bind(MultithreadedChatServerTCP.serverAdd)
        connectionSocket.listen(10)
        
        # Dictionary that holds client's data
        client_db = {}
        # Dictionary that holds active connections
        clients = {}
        lock = threading.Lock()
        clients_lock = threading.Lock()
        
        print(f"Server is waiting for clients on port: {MultithreadedChatServerTCP.PORT}")

        while True:
            conn, addr = connectionSocket.accept()
            print(f"Received request from {addr}")
            
            sthread = ServerThread(conn, addr, client_db, clients, lock, clients_lock)
            sthread.start()

if __name__ == '__main__':
    MultithreadedChatServerTCP.main()
