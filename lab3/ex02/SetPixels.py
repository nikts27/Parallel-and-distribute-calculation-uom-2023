from PIL import Image
import sys
import time

def setPixels(img):
	# Get width and height of Image
    width, height = img.size

	# Coefficinets of r,g,b to GrayScale
    redShift = 100
    greenShift = 100
    blueShift = 100

	# Iterate through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))

            r = int((r + redShift)%256)
            g = int((g + greenShift)%256) 
            b = int((b + blueShift)%256) 
            
            img.putpixel( (x, y), (r, g, b, 255) ) 
    return img

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
    start = time.time()

    # call function
    new = setPixels(img)
    
    # Stop timing
    elapsed_time = (time.time() - start) * 1000

    # Write Image
    new = new.save(fileNameW)
    
    print("Done...")
    print("Time in ms =", elapsed_time)