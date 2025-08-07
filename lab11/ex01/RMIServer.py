# use Python remote object library
import Pyro5.api as pyro

@pyro.expose
class RemoteObject:
    
    def compute_math(self, n1, n2, opp):
        #check for right data
        try:
            a = float(n1)
            b = float(n2)
        except ValueError:
            return 'Not right data given from client. Try again'
                
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

if __name__ == '__main__':
    # Create a Pyro daemon
    daemon = pyro.Daemon()

    # Register the remote object with a name
    uri = daemon.register(RemoteObject)
    
    # Register the object with the name server
    ns = pyro.locate_ns()  # locate the name server
    ns.register("example.remoteobject", uri)  # register the object with a name
    
    # Start the event loop of the server to wait for calls
    daemon.requestLoop()
