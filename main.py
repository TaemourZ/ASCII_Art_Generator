from PIL import Image
import numpy as np
import argparse
import cv2
import os
import shutil

"""
# gray scale level values from:
# https://www.a1k0n.net/2011/07/20/donut-math.html
global charscale
charscale = " .,-~:;=!*#$@"
"""

def videoConverter(inVideo, fps, outName, invert):
    # Create output directory
    outPath = "./" + outName

    if os.path.isdir(outPath):
        shutil.rmtree(outPath) #delete directory if already exists
    
    
    os.mkdir(outPath)

    # Input video
    video = cv2.VideoCapture(inVideo)
    print("FPS:", video.get(cv2.CAP_PROP_FPS))

    # Iterate over frames (fps is how frequent you want frames selected)
    frameCount = 0
    video.set(cv2.CAP_PROP_POS_FRAMES, frameCount)
    ret, frame = video.read()

    while ret:

        color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)

        asciiFrame = asciiOutput(pil_image, invert)
        
        outFile = outPath + '/' + str(frameCount) + '.txt'
        out = open(outFile, 'w')
        for row in asciiFrame:
            out.write(row + '\n')
        out.close()
        
        frameCount += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, frameCount * fps)
        ret, frame = video.read()

    #cv2.destroyAllWindows()
    #os.rmdir(outPath)
    
    return 0

def averageBrightness(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))
    

def asciiOutput(inFile, invert):
    outSize = 100
    if invert:
        charscale = " .,-~:;=!*#$@"
    else:
        charscale = " .,-~:;=!*#$@"[::-1]


    # open image and convert to grayscale
    image = inFile.convert('L')
 
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
    print("TILE DIMS:\t%d x %d" % (w, h))
    print("__________________")
    """

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    aimg.append("")
    for i in range(rows):
        y1 = int(i*h)
        y2 = int((i+1)*h)
        if i == rows-1:
            y2 = H
        
        aimg.append("")
 
        for j in range(outSize):
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

    videoConverter("skeleton.mp4", 5, "skeleton", False)

    parser = argparse.ArgumentParser(
    description="Converts an image to an output text file containing an ASCII art approximation of the input.",
    epilog="usage: python3 main.py -i [input] -o [ouput] -t")
    parser.add_argument('-i', '--input', dest = 'inputImg', help = "path to the input file", required = True)
    parser.add_argument('-o', '--output', dest = 'outFile', help = "output file path for the ASCII art [default = out.txt]", required = False)
    parser.add_argument('-v', '--invert', dest = 'invert', help = "invert brightness of ASCII output", action = 'store_true')
    parser.add_argument('-t', '--terminal', dest = 'terminal', help = "print ASCII art to terminal", action = 'store_true')

    # Parse and process arguments
    args = parser.parse_args()

    inputImg = Image.open(args.inputImg)

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    print('START...')
    asciiImg = asciiOutput(inputImg, args.invert)

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

