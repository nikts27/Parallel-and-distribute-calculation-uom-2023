from PIL import Image
import sys
import time

def rgbToGrey(img):
	# Get width and height of Image
    width, height = img.size

	# Coefficinets of r,g,b to GrayScale
    redCoefficient = 0.299
    greenCoefficient = 0.587
    blueCoefficient = 0.114

	# Iterate through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))

            r = int(r * redCoefficient)
            g = int(g * greenCoefficient) 
            b = int(b * blueCoefficient) 
            
            grey = r+b+g
            
            img.putpixel( (x, y), (grey, grey, grey, 255) ) 
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
    new = rgbToGrey(img)
    
    # Stop timing
    elapsed_time = (time.time() - start) * 1000

    # Write Image
    new = new.save(fileNameW)
    
    print("Done...")
    print("Time in ms =", elapsed_time)