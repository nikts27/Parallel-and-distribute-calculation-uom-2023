import time

# Printing utility
def printResult(v, size, z):
    result = str(z) + ":"
    
    for i in range(size):
        if (v[i]):
            result += " 1"
        else:
            result += " 0"
    
    print(result)
    

def check_circuit(z, size):
    
    # z: the combination number
    # v: the combination number in binar format 
    
    v = []
    v = [False] * size
    
    for i in range(size-1, -1, -1):
        v[i] = (z & (1 << i)) != 0
    
    # Check the ouptut of the circuit for input v
    value = (v[0] or v[1]) and (not v[1] or not v[3]) and (v[2] or v[3]) and \
        (not v[3] or not v[4]) and (v[4] or not v[5]) and (v[5] or not v[6]) and \
        (v[5] or v[6]) and (v[6] or not v[15]) and (v[7] or not v[8]) and \
        (not v[7] or not v[13]) and (v[8] or v[9]) and (v[8] or not v[9]) and \
        (not v[9] or not v[10]) and (v[9] or v[11]) and (v[10] or v[11]) and \
        (v[12] or v[13]) and (v[13] or not v[14]) and (v[14] or v[15]) and \
        (v[14] or v[16]) and (v[17] or v[1]) and (v[18] or not v[0]) and \
        (v[19] or v[1]) and (v[19] or not v[18]) and (not v[19] or not v[9]) and \
        (v[0] or v[17]) and (not v[1] or v[20]) and (not v[21] or v[20]) and \
        (not v[22] or v[20]) and (not v[21] or not v[20]) and (v[22] or not v[20])
    
    # If output == 1 print v and z
    if (value):
        printResult(v, size, z)

if __name__ == '__main__':
    
    # Circuit input size (number of bits)
    size = 28
    # Number of possible inputs (bit combinations)
    iterations = 2 ** size
    
    #start timer
    start = time.time()
    
    # Check all possible inputs
    for i in range(iterations):
        check_circuit(i, size)
        
    # Stop timing
    elapsed_time = (time.time() - start) * 1000
    
    print("Done...")
    print("Time in ms =", elapsed_time)