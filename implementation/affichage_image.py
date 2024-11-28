import cv2
import matplotlib.pyplot as plt

# Charger une image en niveaux de gris
image_original = cv2.imread('image.jpg', cv2.IMREAD_COLOR)

image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Afficher l'image
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image_original, cmap='gray')
plt.title("Image original")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(image, cmap='gray')
plt.title("Image en Niveaux de Gris")
plt.axis('off')

plt.show()


# Afficher les dimensions et la taille d'une image
print(f"Dimensions de l'image : {image.shape}")
print(f"Résolution (hauteur × largeur) : {image.shape[0]} × {image.shape[1]}")
print(f"Taille en mémoire : {image.size * image.itemsize} octets")


import numpy as np

# Réduire la profondeur de bits d'une image (quantification)
quantified_image = (image // 64) * 64  # Réduction à 4 niveaux d'intensité

# Afficher l'image quantifiée
plt.imshow(quantified_image, cmap='gray')
plt.title("Image Quantifiée")
plt.axis('off')
plt.show()


# Ajouter un bruit gaussien
noisy_image = image + np.random.normal(0, 25, image.shape).astype(np.uint8)

# Appliquer un filtre gaussien pour réduire le bruit
denoised_image = cv2.GaussianBlur(noisy_image, (15, 15), 0)

# Affichage
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(noisy_image, cmap='gray')
plt.title("Image Bruitée")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(denoised_image, cmap='gray')
plt.title("Image Débruitée")
plt.axis('off')

plt.show()



# Charger une image en couleurs
color_image = cv2.imread('image.jpg')
color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)  # Conversion BGR -> RGB

# Afficher les canaux R, G, B
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors = ['Rouge', 'Vert', 'Bleu']
for i, ax in enumerate(axes):
    channel = color_image_rgb[:, :, i]
    ax.imshow(channel, cmap='gray')
    ax.set_title(f"Canal {colors[i]}")
    ax.axis('off')
plt.show()




# Appliquer une égalisation d'histogramme
equalized_image = cv2.equalizeHist(image)

# Afficher l'image originale et améliorée
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title("Image Originale")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(equalized_image, cmap='gray')
plt.title("Image avec Contraste Amélioré")
plt.axis('off')

plt.show()
