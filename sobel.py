from PIL import Image as im
import numpy as np

def sobel(image):
    # Convert the image to grayscale
    image = image.convert('L')
    # Convert the image to a numpy array
    image = np.array(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] > 127:
                image[i][j] = 255
            else:
                image[i][j] = 0

    # Apply the Sobel filter
    # Convert the image to a PIL image
    image = im.fromarray(image)
    return image


img = im.open('image.png')

sobel(img).show()

