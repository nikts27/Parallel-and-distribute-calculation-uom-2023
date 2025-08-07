import sys
import time

# find any matches between the text and the pattern
def brute_force_string_match(text, pattern):
    n = len(text)
    m = len(pattern)
    
    match_length = n - m
    match_count = 0
    matches = []
    
    # try to find any matches between the text and the pattern
    for j in range(match_length):
        i = 0
        while i < m and pattern[i] == text[i + j]:
            i += 1
            if i >= m:
                matches.append(j)
                match_count += 1
    
    return matches, match_count
 
if __name__ == "__main__":

    # command line arguments
    if len(sys.argv) != 3:
        print("Usage: python BruteForceStringMatch.py <file name> <pattern>") 
        sys.exit(1)
        
    t1 = time.perf_counter()   
        
    # read the text from the file
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    file_string = None

    for encoding in encodings_to_try:
        try:
            with open(sys.argv[1], 'r', encoding=encoding) as file:
              file_string = file.read()
            break
        except UnicodeDecodeError:
            continue

    if file_string is None:
        print("Failed to decode the file with available encodings.")
        sys.exit(1) 

    text = list(file_string)
    
    # read the search pattern 
    pattern_string = sys.argv[2]
    pattern = list(pattern_string)
    
    matches, match_count = brute_force_string_match(text, pattern)
    
    t2 = time.perf_counter()
    
    # print results
    if match_count == 0:
        print("No matches")
    else:
        for match in matches:
            print(str(match) + " ")
        print("Total matches: " + str(match_count))
    print("Time to compute = " + str(t2-t1) + " seconds")