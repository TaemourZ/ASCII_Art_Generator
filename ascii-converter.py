from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import argparse
import cv2
import os
import shutil

# gray scale level values from:
# https://www.a1k0n.net/2011/07/20/donut-math.html


"""
parameters:
    inVideo: path to input video
    outName: name of the output file
    invert: True to invert brightness of output. False otherwise
    contrastFactor: used to increase and decrease contrast of image before converting
    frameStep: controls how far apart extracted frames are from each other

    RETURNS: 0, and saves the output ASCII gif to device.
"""
def videoConverter(inVideo, outName, invert, contrastFactor, frameStep):
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

        asciiArray = asciiOutput(pil_image, invert, 100, 2.5, contrastFactor) # Convert frame to ascii
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

"""
parameters:
    image: PIL Image object

    RETURNS: value of the average brightness of the input image
"""
def averageBrightness(image):
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))

"""
parameters:
    inFile: path to input file
    invert: True to invert brightness of output. False otherwise
    outSize: number of columns the input image will be split into, and in turn the length of one row in the ASCII output
    scale: used to calculate the height of one cell relative to the width
    contrastFactor: used to increase and decrease contrast of image before converting

    RETURNS: list of strings that make up the ASCII output
""" 
def asciiOutput(inFile, invert, outSize, scale, contrastFactor):
    if invert:
        charScale = " .,-~:;=!*#$@"
    else:
        charScale = " .,-~:;=!*#$@"[::-1]

    enhancer = ImageEnhance.Contrast(inFile) # increase contrast
    image = enhancer.enhance(contrastFactor)
 
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

# main
def main():
    
    parser = argparse.ArgumentParser(description="Converts an image or video into ASCII art.")
    parser.add_argument('-i', '--input', dest = 'inFile', help = "path to the input file", required = True)
    parser.add_argument('-o', '--output', dest = 'outFile', help = "output file name for the ASCII art [.txt for image, .gif for video]", required = True)
    parser.add_argument('-s', '--size', dest = 'outSize', help = "[IMAGE MODE] size of ASCII art output [default = max = 100]", required = False) # Number of columns of output. Number of rows is dependant on number of columns
    parser.add_argument('-c', '--scale', dest = 'scale', help = "[IMAGE MODE] ratio of height to width of text font [default = 2.5]", required = False)
    parser.add_argument('-t', '--contrast', dest = 'contrast', help = "controls contrast of the input image. [default = 1, value must be >= 0]", required = False)
    parser.add_argument('-f', '--frameStep', dest = 'step', help = "[VIDEO MODE] measure of how frequently frames should be selected when converting videos [default = 4, minimum = 1]", required = False)
    parser.add_argument('-v', '--invert', dest = 'invert', help = "invert brightness of ASCII output", action = 'store_true')

    # Parse arguments
    args = parser.parse_args()
    contrast = 1
    if args.contrast:
        contrast = float(args.contrast)

    if (args.inFile.endswith(".mp4") or args.inFile.endswith(".mov")):

        frameStep = 4
        if args.step:
            frameStep = int(args.step)
        
        if frameStep <= 1:
            frameStep = 1

        # Process mp4 file
        print("Starting video conversion...")

        videoConverter(args.inFile, args.outFile, args.invert, contrast, frameStep)

        print("Exiting program.\n")
        exit()
    
    else:
        outSize = 100
        if args.outSize:
            outSize = int(args.outSize)
        
        if outSize >= 100:
            outSize = 100
        
        scale = 2.5
        if args.scale:
            scale = float(args.scale)

        # Process image file
        print("Starting image conversion...")

        image = Image.open(args.inFile).convert('L')
        asciiImg = asciiOutput(image, args.invert, outSize, scale, contrast)

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


