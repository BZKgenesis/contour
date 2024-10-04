Le fichier `sobel.py` implémente l'algorithme de filtrage de Sobel pour la détection des contours dans les images. Voici une explication détaillée du processus :

1. **Chargement et conversion de l'image** :
   ```python
   img = Image.open(image_path).convert('L')
   ```
   - L'image est chargée depuis le chemin spécifié et convertie en niveaux de gris.

2. **Conversion en tableau NumPy** :
   ```python
   img_array = np.array(img, dtype='int32')
   ```
   - L'image est convertie en un tableau NumPy pour faciliter les opérations matricielles.

3. **Définition des kernels de Sobel** :
   ```python
   sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
   sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
   ```
   - Les kernels de Sobel pour les gradients horizontaux (`sobel_x`) et verticaux (`sobel_y`) sont définis.

4. **Initialisation des gradients** :
   ```python
   gradient_x = np.zeros_like(img_array)
   gradient_y = np.zeros_like(img_array)
   ```
   - Des tableaux pour stocker les gradients horizontaux et verticaux sont initialisés.

5. **Application du filtre de Sobel** :
   ```python
   for i in range(1, height-1):
       for j in range(1, width-1):
           region = img_array[i-1:i+2, j-1:j+2]
           gx = np.sum(sobel_x * region)
           gy = np.sum(sobel_y * region)
           gradient_x[i, j] = gx
           gradient_y[i, j] = gy
   ```
   - Les gradients sont calculés pour chaque pixel en appliquant les kernels de Sobel sur une région 3x3 autour de chaque pixel.

6. **Calcul du gradient final** :
   ```python
   gradient = np.sqrt(gradient_x**2 + gradient_y**2)
   ```
   - La magnitude du gradient est calculée en combinant les gradients horizontaux et verticaux.

7. **Normalisation et suppression des non-maxima** :
   ```python
   gradient_x_norm = gradient_x / gradient
   gradient_y_norm = gradient_y / gradient
   for i in range(1, height-1):
       for j in range(1, width-1):
           if not np.isnan(gradient_x_norm[i,j]) and (gradient_x[i, j] < gradient_y[i + round(gradient_x_norm[i,j]), j + round(gradient_y_norm[i,j])] and gradient_x[i, j] < gradient_y[i - round(gradient_x_norm[i,j]), j - round(gradient_y_norm[i,j])]):
               gradient[i, j] = 0
   ```
   - Les gradients sont normalisés et une suppression des non-maxima est appliquée pour affiner les contours.

8. **Normalisation des gradients pour l'affichage** :
   ```python
   gradient_x = np.abs(gradient_x)
   gradient_y = np.abs(gradient_y)
   gradient_x = gradient_x.astype(np.uint8)
   gradient_y = gradient_y.astype(np.uint8)
   ```
   - Les gradients sont normalisés pour être dans la plage [0, 255] et convertis en entier non signé de 8 bits.

9. **Création de l'image en couleur** :
   ```python
   colored_image = np.zeros((height, width, 3), dtype=np.uint8)
   colored_image[..., 0] = gradient_x
   colored_image[..., 1] = gradient_y
   sobel_image = Image.fromarray(colored_image)
   ```
   - Une nouvelle image en couleur est créée en combinant les gradients pour les canaux rouge et vert.

10. **Sauvegarde et mesure des performances** :
    ```python
    img.save("output\\CPUoutput_"+str(i)+".png")
    ```
    - L'image traitée est sauvegardée et les performances de traitement sont mesurées.

En résumé, ce script applique le filtre de Sobel pour détecter les contours dans une image et enregistre les résultats, tout en mesurant le temps de traitement.
