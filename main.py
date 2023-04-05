from PIL import Image
import numpy as np
import argparse

"""
# gray scale level values from:
# https://www.a1k0n.net/2011/07/20/donut-math.html
global charscale
charscale = " .,-~:;=!*#$@"
"""


def averageBrightness(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))
    

def asciiOutput(inFile, outSize, invert):
    if invert:
        charscale = " .,-~:;=!*#$@"
    else:
        charscale = " .,-~:;=!*#$@"[::-1]


    # open image and convert to grayscale
    image = Image.open(inFile).convert('L')
 
    # input image dimensions
    W, H = image.size[0], image.size[1]

    # compute tile dimensions and no. rows
    w = W/outSize
    h = 2 * w
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
        if i == rows-1:
            y2 = H
 
        # append an empty string
        aimg.append("")
 
        for j in range(outSize):
 
            # crop image to tile
            x1 = int(j*w)
            x2 = int((j+1)*w)
            if j == outSize-1:
                x2 = W
 
            # get average brightness of tile
            img = image.crop((x1, y1, x2, y2))
            avg = int(averageBrightness(img))
 
            # add ascii char to list
            gsval = charscale[int((avg*12)/255)]
            aimg[i] += gsval
     
    # return txt image
    return aimg

def main():
    parser = argparse.ArgumentParser(
    description="Converts an image to an output text file containing an ASCII art approximation of the input.",
    epilog="usage: python3 main.py -i [input] -o [ouput] -t")
    parser.add_argument('-i', '--input', dest = 'inputImg', help = "path to the input file", required = True)
    parser.add_argument('-o', '--output', dest = 'outFile', help = "output file path for the ASCII art [default = out.txt]", required = False)
    parser.add_argument('-s', '--size', dest = 'size', help = "number of columns for output ASCII art [default = 50]", required = False)
    parser.add_argument('-v', '--invert', dest = 'invert', help = "invert brightness of ASCII output", action = 'store_true')
    parser.add_argument('-t', '--terminal', dest = 'terminal', help = "print ASCII art to terminal", action = 'store_true')

    args = parser.parse_args()

    inputImg = args.inputImg

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    size = 50
    if args.size:
        size = int(args.size)

    print('START...')
    asciiImg = asciiOutput(inputImg, size, args.invert)

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
- invert colors
- input video
- play ASCII video
- port?
"""
    
    









