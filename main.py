from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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

def videoConverter(inVideo, outName, invert):
    frameStep = 4
    # Create output directory
    outPath = "./" + outName

    # Input video
    video = cv2.VideoCapture(inVideo)
    duration = video.get(cv2.CAP_PROP_FRAME_COUNT)/video.get(cv2.CAP_PROP_FPS)

    # Split video into frames
    frameCount = 0
    images = []
    video.set(cv2.CAP_PROP_POS_FRAMES, frameCount)
    ret, frame = video.read()

    font = ImageFont.truetype("Menlo-Regular.ttf", 10) # Font for ascii output
    
    while ret:
        percentDone = int((frameCount * frameStep)/video.get(cv2.CAP_PROP_FRAME_COUNT) * 100) # show how many frames left to process
        print("Processing... [" + str(percentDone) + "%]")

        color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert cv2 image to PIL
        pil_image = Image.fromarray(color_coverted).convert('L')

        asciiArray = asciiOutput(pil_image, invert, 100, 2.5) # Convert frame to ascii
        rows = len(asciiArray)
        outStr = ''
        for line in asciiArray:
            outStr += line + '\n'

        # Save ascii output to image
        tempImage = Image.new('RGB', (int(pil_image.size[0]/2), int(pil_image.size[1]/2)))
        draw = ImageDraw.Draw(tempImage)
        draw.text((0, 0), outStr, font = font, align ="left")
        images.append(tempImage) # add images to list

        # Advance to next frame
        frameCount += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, frameCount * frameStep)
        ret, frame = video.read()

    print("Processing... [100%]")

    # Combine images to gif
    images[0].save(outName + '.gif', save_all=True,optimize=False, append_images=images[1:], duration = int(duration/1000), loop=0)
    print("Saved " + outName + ".gif")

    return 0

def averageBrightness(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))
    
def asciiOutput(inFile, invert, outSize, scale):
    if invert:
        charScale = " .,-~:;=!*#$@"
    else:
        charScale = " .,-~:;=!*#$@"[::-1]

    enhancer = ImageEnhance.Contrast(inFile) # increase contrast
    image = enhancer.enhance(1.5)
 
    # input image dimensions
    W, H = image.size[0], image.size[1]

    # compute tile dimensions and no. rows
    w = W/outSize
    h = scale * w
    rows = int(H/h)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    aimg.append("")
    for i in range(rows):
        y1 = int(i*h)
        y2 = int((i+1)*h)
        if (i == rows - 1):
            y2 = H
        
        aimg.append("")
 
        for j in range(outSize):
            x1 = int(j*w)
            x2 = int((j+1)*w)
            if (j == outSize - 1):
                x2 = W
 
            # get average brightness of tile
            img = image.crop((x1, y1, x2, y2))
            avg = int(averageBrightness(img))
 
            # add ascii char to list
            aimg[i] += charScale[int((avg*12)/255)]
     
    # return txt image
    return aimg

def main():
    
    parser = argparse.ArgumentParser(
    description="Converts an image or video into ASCII art.",
    epilog="usage: python3 main.py -i [input] -o [ouput] -v")
    parser.add_argument('-i', '--input', dest = 'inFile', help = "path to the input file", required = True)
    parser.add_argument('-o', '--output', dest = 'outFile', help = "output file name for the ASCII art [.txt for image, .gif for video]", required = True)
    parser.add_argument('-s', '--size', dest = 'outSize', help = "size of ASCII art output [default = 100]", required = False)
    parser.add_argument('-c', '--scale', dest = 'scale', help = "ratio of height to width of text font [default = 2.5]", required = False)
    parser.add_argument('-v', '--invert', dest = 'invert', help = "invert brightness of ASCII output", action = 'store_true')

    # Parse arguments
    args = parser.parse_args()

    if (args.inFile.endswith(".mp4")):
        # Process mp4 file
        print("Starting video conversion...")

        videoConverter(args.inFile, args.outFile, args.invert)

        print("Exiting program.\n")
        exit()
    
    else:
        outSize = 100
        if args.outSize:
            outSize = int(args.outSize)
        
        scale = 2.5
        if args.scale:
            scale = float(args.scale)

        # Process image file
        print("Starting image conversion...")

        image = Image.open(args.inFile).convert('L')
        asciiImg = asciiOutput(image, args.invert, outSize, scale)

        # Write to output file
        out = open(args.outFile + ".txt", 'w')
        for row in asciiImg:
            out.write(row + '\n')
        out.close()

        print("Saved " + args.outFile + ".txt")
        print("Exiting program.\n")
        exit()
    
    return 0
    
if __name__ == '__main__':
    main()


