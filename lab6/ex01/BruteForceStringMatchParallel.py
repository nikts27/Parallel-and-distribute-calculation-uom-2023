import sys
import time
import threading
import multiprocessing

# find any matches between the text and the pattern in a specific range
def find_matches(block):
    start, stop, text, pattern, pattern_length = block
    local_match_count = 0
    local_matches = []

    for j in range(start, stop - pattern_length + 1):
        k = 0
        while k < pattern_length and pattern[k] == text[j + k]:
            k += 1
        if k == pattern_length:
            local_matches.append(j)
            local_match_count += 1

    return local_match_count, local_matches

if __name__ == "__main__":
    
    # check command line arguments
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
    
    n = len(text)
    m = len(pattern)
    num_threads = multiprocessing.cpu_count()
    block_size = n // num_threads

    # Prepare blocks
    blocks = []
    for i in range(num_threads):
        start = i * block_size
        stop = min((i + 1) * block_size, n)
        blocks.append((start, stop, text, pattern, m))

    # Create and start threads
    threads = []
    results = []
    for block in blocks:
        thread = threading.Thread(target=lambda: results.append(find_matches(block)))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Process results
    match_count = sum(local_match_count for local_match_count, _ in results)
    all_matches = [match for _, local_matches in results for match in local_matches]

    t2 = time.perf_counter()

    # Print results
    if match_count == 0:
        print("No matches")
    else:
        for match in all_matches:
            print(match)
        print("Total matches: " + str(match_count))
    print("Time to compute = " + str(t2 - t1) + " seconds")
