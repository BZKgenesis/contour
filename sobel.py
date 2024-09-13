from PIL import Image as im, ImageColor as imc
import cv2
import numpy as np
import time
from math import sqrt

def difference (img,i,j,x,y):
    _XoffsetP = i+x
    _XoffsetL = i-x
    _YoffsetP = j+y
    _YoffsetL = j-y
    return img[_XoffsetP][_YoffsetP]/256 - img[_XoffsetL][_YoffsetL]/256

def sobelX(img,x,y):
    return -2*img[x-1][y] + 2*img[x+1][y] - img[x-1][y-1] + img[x+1][y-1] - img[x-1][y+1] + img[x+1][y+1]

def sobelY(img,x,y):
    return -2*img[x][y+1] + 2*img[x][y-1] - img[x-1][y+1] + img[x+1][y+1] - img[x-1][y-1] + img[x+1][y-1]

def clamp(v,min,max):
    if v < min:
        return min
    elif v > max:
        return max
    else:
        return v

def sobel(image):
    image = np.asarray(image.convert('L'), dtype="float64")
    _img = np.asarray(im.new('RGB',(image.shape[1],image.shape[0]),1 ), dtype="float64")
    print(_img.shape)
    print(image.shape)
    for i in range(1,_img.shape[0]-1):
        for j in range(1,_img.shape[1]-1):
            #print(image.shape[0], image.shape[1] , i , j)
            x = sobelX(image,i,j)
            y = sobelY(image,i,j)
            dist = sqrt(x**2 + y**2)
            _img[i][j] = x
            _img[i][j] = y
    #_img*=256
    #_img = _img.astype(np.uint8)
    _img = im.fromarray(_img, mode='RGB')
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

