import random
import multiprocessing

# calculate for each subproblem
def estimatePiPerBlock(interval, i, num_processes, circle_points, square_points, lock_circle, lock_square):
    
    local_square = 0
    local_circle = 0
   
    block = interval**2//num_processes
    start = i * block
    stop = start + block
    if i==num_processes-1:
        stop = interval**2
    
    for j in range(start, stop):
        # Randomly generated x and y values from a
        # uniform distribution
        # Range of x and y values is -1 to 1
        rand_x = random.uniform(-1, 1)
        rand_y = random.uniform(-1, 1)
 
        # Distance between (x, y) from the origin
        origin_dist = rand_x**2 + rand_y**2
 
        # Checking if (x, y) lies inside the circle
        if origin_dist <= 1:
           local_circle += 1
 
        local_square += 1
    
    with lock_circle:
        circle_points.value += local_circle
    
    with lock_square:
        square_points.value += local_square
    
    

if __name__ == "__main__":
    
    INTERVAL = 1000

    # Get the number of CPU cores
    num_processes = multiprocessing.cpu_count()
    processes = []
    
    # Create 2 locks (one for each element we want to calculate)
    lock_circle = multiprocessing.Lock()
    lock_square = multiprocessing.Lock()
    
    circle_points_ref = multiprocessing.Value('d', 0.0)
    square_points_ref = multiprocessing.Value('d', 0.0)
 
    #create processes
    for i in range(num_processes):
        p = multiprocessing.Process(target=estimatePiPerBlock, args=(INTERVAL, i, num_processes, circle_points_ref, square_points_ref,
                                                                     lock_circle, lock_square))
        processes.append(p)
    
    # start processes
    for p in processes:
        p.start()
    
    # wait for processes to finish
    for p in processes:
        p.join()
    
    # Estimating value of pi,
    # pi= 4*(no. of points generated inside the
    # circle)/ (no. of points generated inside the square)
    pi = 4 * circle_points_ref.value / square_points_ref.value
    
    print("Final Estimation of Pi=", pi)