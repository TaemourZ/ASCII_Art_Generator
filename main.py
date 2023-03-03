import cv2

# Input image
print("Enter image: ", end = '')
image = input()
default = 'homapage.jpeg'
image = cv2.imread("./" + default)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Increase contrast
contrast_gray = cv2.convertScaleAbs(gray, 200, 1.2)

# Pixelate image. Hacky solution, work on it more

# Set size of pixels
height = gray.shape[0]
width = gray.shape[1]
# print(height, width)

w, h = (int(height/3), int(width/3))

# Resize input to "pixelated" size
temp = cv2.resize(contrast_gray, (w, h), interpolation=cv2.INTER_LINEAR)
output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)


# Display images
cv2.imshow('Original image',image)
cv2.waitKey(0)
cv2.imshow('Grayscale', gray)
cv2.waitKey(0)
cv2.imshow('Contrast Up', contrast_gray)
cv2.waitKey(0)
cv2.imshow('Pixelated', output)
cv2.waitKey(0)


cv2.destroyAllWindows()