import math

def convolution(image, kernel):
    hauteur_image = len(image)
    largeur_image = len(image[0])
    hauteur_kernel = len(kernel)
    largeur_kernel = len(kernel[0])
    offset_h = hauteur_kernel // 2
    offset_w = largeur_kernel // 2

    resultat = [[0 for _ in range(largeur_image)] for _ in range(hauteur_image)]

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

def magnitude_and_direction(gradient_x, gradient_y):
    hauteur = len(gradient_x)
    largeur = len(gradient_x[0])
    magnitude = [[0 for _ in range(largeur)] for _ in range(hauteur)]
    direction = [[0 for _ in range(largeur)] for _ in range(hauteur)]

    for i in range(hauteur):
        for j in range(largeur):
            gx = gradient_x[i][j]
            gy = gradient_y[i][j]
            magnitude[i][j] = math.sqrt(gx**2 + gy**2)
            direction[i][j] = math.atan2(gy, gx)
    return magnitude, direction

def suppression_non_maxima(magnitude, direction):
    hauteur = len(magnitude)
    largeur = len(magnitude[0])
    resultat = [[0 for _ in range(largeur)] for _ in range(hauteur)]

    for i in range(1, hauteur - 1):
        for j in range(1, largeur - 1):
            angle = direction[i][j]
            q = 255
            r = 255

            # Approximation des directions en 0, 45, 90, 135 degrés
            if (0 <= angle < math.pi / 4) or (-math.pi < angle < -3 * math.pi / 4):
                q = magnitude[i][j + 1]
                r = magnitude[i][j - 1]
            elif (math.pi / 4 <= angle < 3 * math.pi / 4):
                q = magnitude[i + 1][j]
                r = magnitude[i - 1][j]

            if magnitude[i][j] >= q and magnitude[i][j] >= r:
                resultat[i][j] = magnitude[i][j]
            else:
                resultat[i][j] = 0

    return resultat

def seuillage_hysteresis(image, bas, haut):
    hauteur = len(image)
    largeur = len(image[0])
    resultat = [[0 for _ in range(largeur)] for _ in range(hauteur)]

    for i in range(1, hauteur - 1):
        for j in range(1, largeur - 1):
            if image[i][j] >= haut:
                resultat[i][j] = 255
            elif image[i][j] < bas:
                resultat[i][j] = 0
            else:
                if any(image[ni][nj] >= haut for ni in range(i - 1, i + 2) for nj in range(j - 1, j + 2)):
                    resultat[i][j] = 255
                else:
                    resultat[i][j] = 0
    return resultat

# Filtre Canny
def filtre_canny(image, seuil_bas, seuil_haut):
    # 1. Floutage avec un filtre gaussien
    filtre_gaussien = [
        [1/16, 2/16, 1/16],
        [2/16, 4/16, 2/16],
        [1/16, 2/16, 1/16]
    ]
    image_floutee = convolution(image, filtre_gaussien)

    # 2. Calcul des gradients avec les filtres de Sobel
    filtre_sobel_x = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    filtre_sobel_y = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ]
    gradient_x = convolution(image_floutee, filtre_sobel_x)
    gradient_y = convolution(image_floutee, filtre_sobel_y)

    # 3. Magnitude et direction
    magnitude, direction = magnitude_and_direction(gradient_x, gradient_y)

    # 4. Suppression des non-maxima
    suppression = suppression_non_maxima(magnitude, direction)

    # 5. Seuillage par hystérésis
    resultat = seuillage_hysteresis(suppression, seuil_bas, seuil_haut)

    return resultat

# Exemple d'image
image = [
    [10, 20, 30, 40, 50],
    [60, 70, 80, 90, 100],
    [110, 120, 130, 140, 150],
    [160, 170, 180, 190, 200],
    [210, 220, 230, 240, 250],
]





from PIL import Image

def image_to_tableau(image_path):
    """
    Convertit une image en niveaux de gris et retourne un tableau 2D de valeurs entre 0 et 255.
    
    :param image_path: Chemin de l'image à convertir.
    :return: Tableau 2D des niveaux de gris (valeurs entre 0 et 255).
    """
    # Ouvrir l'image
    image = Image.open(image_path)
    
    # Convertir l'image en niveaux de gris
    image_grayscale = image.convert("L")
    
    # Récupérer les dimensions de l'image
    largeur, hauteur = image_grayscale.size
    
    # Convertir en tableau 2D
    tableau = [
        [image_grayscale.getpixel((x, y)) for x in range(largeur)]
        for y in range(hauteur)
    ]
    
    return tableau

from PIL import Image

def tableau_to_image(tableau, output_path):
    """
    Convertit un tableau 2D de valeurs entre 0 et 255 en une image et l'enregistre.

    :param tableau: Tableau 2D (liste de listes) contenant des valeurs entre 0 et 255.
    :param output_path: Chemin où enregistrer l'image générée.
    """
    # Vérifier que toutes les valeurs sont entre 0 et 255
    for row in tableau:
        if any(pixel < 0 or pixel > 255 for pixel in row):
            raise ValueError("Toutes les valeurs du tableau doivent être entre 0 et 255.")
    
    # Dimensions de l'image
    hauteur = len(tableau)
    largeur = len(tableau[0]) if hauteur > 0 else 0

    # Créer une nouvelle image en niveaux de gris
    image = Image.new("L", (largeur, hauteur))

    # Remplir l'image avec les données du tableau
    for y in range(hauteur):
        for x in range(largeur):
            image.putpixel((x, y), int(tableau[y][x]))

    # Enregistrer l'image
    image.save(output_path)
    print(f"Image enregistrée à : {output_path}")


chemin_image = "image.jpg"  # Remplacez par le chemin de votre image
tableau = image_to_tableau(chemin_image)

resultat = filtre_canny(image_to_tableau(chemin_image), seuil_bas=50, seuil_haut=100)

output_path = "resultat_image.png"
tableau_to_image(resultat, output_path)
