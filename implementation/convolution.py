def appliquer_kernel(image, kernel):
    """
    Applique un kernel (matrice) à une image représentée sous forme de liste 2D.

    :param image: Liste 2D représentant les pixels de l'image (grayscale).
    :param kernel: Liste 2D représentant le noyau (kernel).
    :return: Nouvelle image après convolution.
    """
    hauteur_image = len(image)
    largeur_image = len(image[0])
    hauteur_kernel = len(kernel)
    largeur_kernel = len(kernel[0])
    
    # Calcul des décalages pour centrer le kernel
    offset_h = hauteur_kernel // 2
    offset_w = largeur_kernel // 2

    # Image résultat
    resultat = [[0 for _ in range(largeur_image)] for _ in range(hauteur_image)]

    # Convolution
    for i in range(offset_h, hauteur_image - offset_h):
        for j in range(offset_w, largeur_image - offset_w):
            somme = 0
            for ki in range(hauteur_kernel):
                for kj in range(largeur_kernel):
                    pixel = image[i + ki - offset_h][j + kj - offset_w]
                    coeff = kernel[ki][kj]
                    somme += pixel * coeff
            resultat[i][j] = somme

    return resultat

# Exemple d'utilisation
image = [
    [10, 20, 30, 40, 50],
    [60, 70, 80, 90, 100],
    [110, 120, 130, 140, 150],
    [160, 170, 180, 190, 200],
    [210, 220, 230, 240, 250],
]

# Exemple de kernel (noyau de flou moyen 3x3)
kernel = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
]

# Appliquer le kernel
image_resultat = appliquer_kernel(image, kernel)

# Afficher le résultat
for ligne in image_resultat:
    print(ligne)
