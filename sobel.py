from PIL import Image
import numpy as np
import time

#chatGPT

def sobel_filter_with_color_channels(image_path):
    # Charger l'image et la convertir en niveaux de gris
    img = Image.open(image_path).convert('L')
    
    # Convertir l'image en un tableau numpy
    img_array = np.array(img, dtype='int32')
    
    # Définir les kernels de Sobel
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    # Obtenir les dimensions de l'image
    height, width = img_array.shape
    
    # Initialiser les tableaux pour les gradients
    gradient_x = np.zeros_like(img_array)
    gradient_y = np.zeros_like(img_array)
    
    # Appliquer les filtres de Sobel
    for i in range(1, height-1):
        for j in range(1, width-1):
            # Extraire la région 3x3
            region = img_array[i-1:i+2, j-1:j+2]
            
            # Appliquer les kernels de Sobel
            gx = np.sum(sobel_x * region)
            gy = np.sum(sobel_y * region)
            
            # Stocker les gradients
            gradient_x[i, j] = gx
            gradient_y[i, j] = gy
    gradient_x_abs = np.abs(gradient_x)
    gradient_y_abs = np.abs(gradient_y)


    gradient = np.sqrt(gradient_x**2 + gradient_y**2)

    gradient_x_norm = gradient_x / gradient
    gradient_y_norm = gradient_y / gradient

    for i in range(1, height-1):
        for j in range(1, width-1):
            # Extraire la région 3x3
            if not np.isnan(gradient_x_norm[i,j]) and  (gradient_x[i, j] < gradient_y[i + round(gradient_x_norm[i,j]), j + round(gradient_y_norm[i,j])] and gradient_x[i, j] < gradient_y[i - round(gradient_x_norm[i,j]), j - round(gradient_y_norm[i,j])]):
                gradient[i, j] = 0
    
    
    # Normaliser les gradients pour qu'ils soient dans la plage [0, 255]
    gradient_x = np.abs(gradient_x)
    gradient_y = np.abs(gradient_y)

    #gradient = np.sqrt(gradient_x**2 + gradient_y**2)

    #gradient = gradient.astype(np.uint8)
    img = Image.fromarray(gradient)
    
    # Éviter la division par zéro en cas où les max soient 0
    #if gradient_x.max() > 0:
    #    gradient_x = (gradient_x / gradient_x.max()) * 255
    #if gradient_y.max() > 0:
    #    gradient_y = (gradient_y / gradient_y.max()) * 255

    gradient_x = gradient_x.astype(np.uint8)
    gradient_y = gradient_y.astype(np.uint8)
    
    # Créer une image couleur en combinant les canaux
    # Mettre gradient_x dans le canal rouge et gradient_y dans le canal vert
    colored_image = np.zeros((height, width, 3), dtype=np.uint8)
    colored_image[..., 0] = gradient_x  # Canal rouge
    colored_image[..., 1] = gradient_y  # Canal vert
    
    # Convertir le tableau numpy en image
    sobel_image = Image.fromarray(colored_image)
    
    return img
    #return sobel_image


for i in range(1, 2):
    start = time.time()
    img = sobel_filter_with_color_channels(str(i)+".png")
    end = time.time()
    elapsed = end - start
    print("img "+str(i)+" : ", round (elapsed * 1000), "ms")
    img.save("output\\CPUoutput_"+str(i)+".png")


"""
specs:
CPU:i5-12450H
RAM:8,00 Go
GPU: Intel(R) UHD Graphics


perfs:
img 1 :  2326 ms (2s 326 ms)
img 2 :  1843 ms (1s 843 ms)
img 3 :  5672 ms (5s 672 ms)
img 4 :  131428 ms (2min 11s 428 ms)
"""