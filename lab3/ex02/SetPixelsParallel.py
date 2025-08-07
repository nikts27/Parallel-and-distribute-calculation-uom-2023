from PIL import Image
import sys
import time
import multiprocessing

def convertPixels(start, stop, img, rs, gs, bs):
    width, height = img.size
    output = Image.new('RGB', (width, height))  # Create a new output image

    # Iterate over the specified range of pixels
    for x in range(start, stop):
        for y in range(height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))

            r = int((r + rs)%256)
            g = int((g + gs)%256) 
            b = int((b + bs)%256)
                        
            output.putpixel( (x, y), (r, g, b, 255) )
    return output
    

def setPixels(img):
	# Get width and height of Image
    width, height = img.size

	# Coefficinets of r,g,b
    redShift = 100
    greenShift = 100
    blueShift = 100
    
    # Get the number of CPU cores
    num_processes = multiprocessing.cpu_count()
    
    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=num_processes)

    block = height // num_processes
    results = []

	# Divide the image vertically into parts and process each part in parallel
    for i in range(num_processes):
        start = i * block
        end = start + block
        if i == num_processes - 1:
            end = height
         # Pass a cropped part of the image to each process for conversion
        results.append(pool.apply_async(convertPixels, args=(0, width, img.crop((0, start, width, end)), 
                                                             redShift, greenShift, blueShift,)))

    output_images = [result.get() for result in results]

    # Wait for all processes to finish
    pool.close()
    pool.join()

    # Combine output from different processes into one image
    output = Image.new('RGB', (width, height))
    for i, img_part in enumerate(output_images):
        output.paste(img_part, (0, i * block))

    return output

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("Usage: python RGBtoGrayScale <file to read > <file to write>") 
        sys.exit(1)
    
    fileNameR = sys.argv[1]
    fileNameW = sys.argv[2]
    
    # Read Image
    orig = Image.open(fileNameR)

    # Convert Image into RGB
    img = orig.convert('RGB')
    
    #start timer
    timer = time.time()

    # call function
    new = setPixels(img)
    
    # Stop timing
    elapsed_time = (time.time() - timer) * 1000

    # Write Image
    new = new.save(fileNameW)
    
    print("Done...")
    print("Time in ms =", elapsed_time)