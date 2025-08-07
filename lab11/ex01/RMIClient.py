# use Python remote object library
import Pyro5.api as pyro
import time

# οπως βλέπουμε η υλοποίηση με απομακρυσμένα αντικείμενα είναι πιο απλή σε σχέση με αυτή με υποδοχές.
# Υπάρχουν και στον client και στον server πολύ λιγότερες γραμμές κώδικα, διευκολύνεται η μεταβίβαση πληροφορίας από
# τον client στον server ενώ γίνονται εύκολα και οι έλεγχοι και οι επιστροφές τιμών.
# Υπάρχει, μόνο μια αμελητέα καθυστέρηση στον χρόνο εκτέλεσης που όμως δεν έχει κάποια μεγάλη σημασία.
# Άρα, μπορούμε η υλοποίηση με απομακρυσμένα αντικείμενα είναι πιο απλή σε σχέση με αυτήν με υποδοχές.

if __name__ == '__main__':
    # Locate the remote object by name
    uri = pyro.Proxy("PYRONAME:example.remoteobject")
        
    while True:
        # get user input
        n1 = input("Give first number: ")
        n2 = input("Give second number: ")
        opp = input("Give mathematic act: ")
        
        t1 = time.perf_counter()
    
        # Call the remote method
        result = uri.compute_math(n1, n2, opp)
        
        t2 = time.perf_counter()
        
        print("Result = "+ str(result))
        print('Time to compute = {} seconds'.format(t2 - t1))
        
        # ask the user if it wants to give more expressions
        continue_use = input("Continue using the calculator (Y/N?): ")
        while continue_use != 'Y' and continue_use != 'N':
            print("Not acceptable answer. Try again")
            continue_use = input("Continue using the calculator (Y/N?): ")
        if continue_use == 'N':
            break
