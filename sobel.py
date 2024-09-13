from PIL import Image as im
import numpy as np
import time

def sobel(image):
    image = image.convert('L')
    image = np.array(image)
    _img = image.copy()

    XMat = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    YMat = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

    Gx = np.convolve(np.ndarray.flatten(XMat), np.ndarray.flatten(image))
    Gy = np.convolve(np.ndarray.flatten(YMat), np.ndarray.flatten(image))

    
    for i in range(1,image.shape[0]-1):
        for j in range(1,image.shape[1]-1):
            for k in range(XMat.shape[0]):
                for l in range(XMat.shape[1]):
                    _img[i][j] += XMat[k][l]*image[i+k-1][j+l-1]

    _img = im.fromarray(_img)
    return _img

img = im.open('1.png')
start = time.time()
sobel(img).show()
end = time.time()
elapsed = end - start
print("img 1 : ", elapsed)

img = im.open('2.png')
start = time.time()
sobel(img).show()
end = time.time()
elapsed = end - start
print("img 2 : ", elapsed)

