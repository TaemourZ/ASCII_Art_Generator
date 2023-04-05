from PIL import Image
import numpy as np
import argparse

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/
global charscale
charscale = "@%#*+=-:. "

def averageBrightness(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
 
    # get shape
    w,h = im.shape

    # get average
    return np.average(im.reshape(w*h))

def asciiOutput(inFile, outSize, letterScale):

    # open image and convert to grayscale
    image = Image.open(inFile).convert('L')
 
    # input image dimensions
    W, H = image.size[0], image.size[1]

    # compute tile dimensions and no. rows
    w = W/outSize
    h = w/letterScale
    rows = int(H/h)

    """ Debug stuff
    image.show()
    print("INPUT IMAGE:\twidth: %d \theight: %d" % (W, H))
    print("OUTPUT ASCII:\tcols: %d \trows: %d" % (outSize, rows))
    print("TIME DIMS:\t%d x %d" % (w, h))
    print("__________________")
    """

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for i in range(rows):
        y1 = int(i*h)
        y2 = int((i+1)*h)
 
        # correct last tile
        if i == rows-1:
            y2 = H
 
        # append an empty string
        aimg.append("")
 
        for j in range(outSize):
 
            # crop image to tile
            x1 = int(j*w)
            x2 = int((j+1)*w)
 
            # correct last tile
            if j == outSize-1:
                x2 = W
 
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
 
            # get average luminance
            avg = int(averageBrightness(img))
 
            # look up ascii char
            gsval = charscale[int((avg*9)/255)]
 
            # append ascii char to string
            aimg[i] += gsval
     
    # return txt image
    return aimg

"""
print(np.average([1,2,3,4,5]))
image = 'homapage.jpeg'
arr = asciiOutput(image, 100, 0.43)
for row in arr:
    print(row)
"""
def main():
    parser = argparse.ArgumentParser(
    description="Converts an image to an output text file containing an ASCII art approximation of the input.",
    epilog="usage: python3 main.py -i [input] -o [ouput] -t")
    parser.add_argument('-i', '--input', dest = 'inputImg', help = "path to the input file", required = True)
    parser.add_argument('-o', '--output', dest = 'outFile', help = "output file path for the ASCII art [default = out.txt]", required = False)
    parser.add_argument('-s', '--size', dest = 'size', help = "number of columns for output ASCII art [default = 50]", required = False)
    parser.add_argument('-r', '--ratio', dest = 'ratio', help = "ratio of height/width of text font [default = 0.45]", required = False)
    parser.add_argument('-t', '--terminal', dest = 'terminal', help = "print ASCII art to terminal", action = 'store_true')

    args = parser.parse_args()

    inputImg = args.inputImg

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    size = 50
    if args.size:
        size = int(args.size)

    ratio = 0.45
    if args.ratio:
        ratio = float(args.ratio)

    print('START...')
    asciiImg = asciiOutput(inputImg, size, ratio)

    out = open(outFile, 'w')
    if (args.terminal):
        for row in asciiImg:
            out.write(row + '\n')
            print(row)
    else:
        for row in asciiImg:
            out.write(row + '\n')
    
    out.close()
    print('...DONE')
    
if __name__ == '__main__':
    main()

"""
TBA:
- increase contrast
- input video
- play ASCII video
- port?
"""
    
    









