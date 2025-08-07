# use Python remote object library
import Pyro5.api as pyro

if __name__ == '__main__':
    # Locate the remote object by name
    uri = pyro.Proxy("PYRONAME:example.remoteobject")
    
    while True:
        # get number of steps
        numberOfSteps = input("Enter number of steps of pi calculation (select -1 to finish): ")
        if numberOfSteps == "-1":
            break
    
        # Call the remote method
        result = uri.calc_Pi(numberOfSteps)
        print("Result = "+ str(result))