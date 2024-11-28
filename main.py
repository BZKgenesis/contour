import numpy as np
import os
from PIL import Image
import moderngl
import time
import matplotlib.pyplot as plt
def clear():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

COMPARAISONX = 1. # Séparation de l'image pour pouvoir comparer avec et sans le filtre (0.0 - 1.0)
SEUIL = 1.15 # Seuil de détection des contours (0.0 - 1.0)
BENCHMARK = True # Passer en mode mesure de performance (True) ou en mode rendu (False)

# Création du contexte OpenGL
ctx = moderngl.create_standalone_context()
print("Vendor:", ctx.info['GL_VENDOR'])
print("Renderer:", ctx.info['GL_RENDERER'])
print("Version:", ctx.info['GL_VERSION'])
#print("Shading Language Version:", ctx.info['GL_SHADING_LANGUAGE_VERSION'])

def OpenGlEnv(ImageName, fragmentShaderData, seuil):
    # Charger l'image
    image = Image.open(ImageName).convert('RGB') # on ouvre l'image et on la converti en RGB (pour supprimer le canal alpha si il existe)
    image_data = np.array(image).astype('f4') / 255.0  # Normaliser les couleurs (0.0 - 1.0)
    # f4 : float 32 bits


    # Création de la texture de l'image
    texture = ctx.texture(image.size, 3, (image_data * 255).astype('u1').tobytes()) # on reprend l'image convertie en RGB et on la converti en 8 bits
    #u1 : unsigned int 8 bits (0 - 255)

    texture.build_mipmaps() # Générer les mipmaps pour le filtrage (sa sert a rien dans notre cas)

    # Créer un framebuffer pour le rendu de l'image avec le shader
    fbo = ctx.framebuffer(color_attachments=[ctx.texture(image.size, 3)]) # on crée un framebuffer avec une texture de la taille de l'image
    fbo.use() # on utilise le framebuffer
    # fbo : framebuffer object (objet qui contient les textures de rendu)



    # Création du programme (vertex + fragment shaders)
    prog = ctx.program( # meme vertex shader pour tous car on ne touche pas aux vertex (on ne fait que passer les coordonnées de texture)
        vertex_shader="""
        #version 330
        in vec2 in_vert;
        in vec2 in_texcoord;
        out vec2 v_texcoord;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_texcoord = in_texcoord;
        }
        """,
        fragment_shader=fragmentShaderData
    )  

    prog['Resolution'] = (image.size[0], image.size[1]) # Récupérer la résolution de l'image (pour le calcul de la taille d'un pixel)
    #prog['comparaison'] = (comparaison, 0)  # on passe les paramètres dans le shader
    prog['seuil'] = seuil 

    # Définit la géométrie du rectangle à rendre (un quadrilatère couvrant tout l'écran)
    vertices = np.array([
        # Positions    # Coordonnées de texture
        -1.0,  1.0,    0.0, 1.0,
        -1.0, -1.0,    0.0, 0.0,
        1.0,  1.0,    1.0, 1.0,
        1.0, -1.0,    1.0, 0.0,
    ], dtype='f4') # on défini 2 triangles pour couvrir tout l'écran les coordonnées de géometrie sont en -1, 1 pour couvrir tout l'écran (centre en 0, 0 au milieu de l'écran)
    # les coordonnées de texture sont en 0, 1 pour afficher toute la texture
    #f4 : float 32 bits

    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_texcoord')

    # vbo : vertex buffer object (objet qui contient les données de géométrie)
    # vao : vertex array object (objet qui contient les données de géométrie et le programme


    # Utilisation de la texture et rendu
    texture.use()
    texture.filter = (moderngl.NEAREST, moderngl.NEAREST) # on utilise le filtrage nearest pour éviter les flous (pas d'intérpolation entre les pixels)
    
    vao.render(moderngl.TRIANGLE_STRIP) # on rend le quadrilatère (le type de rendu est TRIANGLE_STRIP car on a défini 2 triangles)

    # Récupérer les données de l'image du framebuffer
    data = fbo.read(components=3) # on récupère les données de l'image (3 composantes RGB)
    output_image = Image.frombytes('RGB', image.size, data) # on crée une image à partir des données récupérées
    output_image = output_image.crop((1, 1, image.size[0]-1, image.size[1]-1)) # on enlève les bords de l'image (qui sont faussés par le filtre)

    # On retourne l'image
    return output_image

def OpenGlEnvCany(ImageName, fragmentShaderData, seuil):
    # Charger l'image
    image = Image.open(ImageName).convert('RGB') # on ouvre l'image et on la converti en RGB (pour supprimer le canal alpha si il existe)
    image_data = np.array(image).astype('f4') / 255.0  # Normaliser les couleurs (0.0 - 1.0)
    # f4 : float 32 bits


    # Création de la texture de l'image
    texture = ctx.texture(image.size, 3, (image_data * 255).astype('u1').tobytes()) # on reprend l'image convertie en RGB et on la converti en 8 bits
    #u1 : unsigned int 8 bits (0 - 255)

    texture.build_mipmaps() # Générer les mipmaps pour le filtrage (sa sert a rien dans notre cas)

    # Créer un framebuffer pour le rendu de l'image avec le shader
    fbo = ctx.framebuffer(color_attachments=[ctx.texture(image.size, 3)]) # on crée un framebuffer avec une texture de la taille de l'image
    fbo.use() # on utilise le framebuffer
    # fbo : framebuffer object (objet qui contient les textures de rendu)



    # Création du programme (vertex + fragment shaders)
    prog = ctx.program( # meme vertex shader pour tous car on ne touche pas aux vertex (on ne fait que passer les coordonnées de texture)
        vertex_shader="""
        #version 330
        in vec2 in_vert;
        in vec2 in_texcoord;
        out vec2 v_texcoord;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_texcoord = in_texcoord;
        }
        """,
        fragment_shader=fragmentShaderData
    )  

    prog['Resolution'] = (image.size[0], image.size[1]) # Récupérer la résolution de l'image (pour le calcul de la taille d'un pixel)
    prog['seuil'] = seuil 

    # Définit la géométrie du rectangle à rendre (un quadrilatère couvrant tout l'écran)
    vertices = np.array([
        # Positions    # Coordonnées de texture
        -1.0,  1.0,    0.0, 1.0,
        -1.0, -1.0,    0.0, 0.0,
        1.0,  1.0,    1.0, 1.0,
        1.0, -1.0,    1.0, 0.0,
    ], dtype='f4') # on défini 2 triangles pour couvrir tout l'écran les coordonnées de géometrie sont en -1, 1 pour couvrir tout l'écran (centre en 0, 0 au milieu de l'écran)
    # les coordonnées de texture sont en 0, 1 pour afficher toute la texture
    #f4 : float 32 bits

    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_texcoord')

    # vbo : vertex buffer object (objet qui contient les données de géométrie)
    # vao : vertex array object (objet qui contient les données de géométrie et le programme


    # Utilisation de la texture et rendu
    texture.use()
    texture.filter = (moderngl.NEAREST, moderngl.NEAREST) # on utilise le filtrage nearest pour éviter les flous (pas d'intérpolation entre les pixels)
    
    vao.render(moderngl.TRIANGLE_STRIP) # on rend le quadrilatère (le type de rendu est TRIANGLE_STRIP car on a défini 2 triangles)

    # Récupérer les données de l'image du framebuffer
    data = fbo.read(components=3) # on récupère les données de l'image (3 composantes RGB)
    output_image = Image.frombytes('RGB', image.size, data) # on crée une image à partir des données récupérées
    output_image = output_image.crop((1, 1, image.size[0]-1, image.size[1]-1)) # on enlève les bords de l'image (qui sont faussés par le filtre)

    # On retourne l'image
    return output_image


def sobelFilter(ImageName, sobelSeuil):
    
    with open ("sobelFilter.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    return OpenGlEnv(ImageName, data,sobelSeuil) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

def prewittFilter(ImageName, prewittSeuil):
    
    with open ("prewittFilter.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    return OpenGlEnv(ImageName, data,prewittSeuil) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

def canyFilter(ImageName, canySeuil,sobelSeuil):
    with open ("sobelFilter.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    OpenGlEnv(ImageName, data, sobelSeuil).save(ImageName[:-4] + "_temp.png")
    
    with open ("canyFilter.frag", "r") as myfile:
        data = myfile.read()
    
        
    return OpenGlEnvCany(ImageName[:-4] + "_temp.png", data,canySeuil) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

def canyTest(ImageName, canySeuil):
    with open ("canyFilter.frag", "r") as myfile:
        data = myfile.read()
    
        
    return OpenGlEnvCany(ImageName, data,canySeuil) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

def differenceGaussian(ImageName):
    
    with open ("differenceGauss.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    return OpenGlEnv(ImageName, data,0) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

    
execution_times = {}
rep = ""
input_file = ""

filtre_choice = 0

print("Bienvenue dans le programme de détection de contours !")
print("images disponibles par défault:")
for i in range(1, 10):
    print("nom: \""+str(i) + "\" résolution: ("+ str(Image.open(str(i)+".png").size[0]) + "x"+ str(Image.open(str(i)+".png").size[1]) +")")

input_file = input("Entrez le nom de l'image d'entrée (sans l'extension) : ") + ".png"
clear()

print("1. Filtre de Sobel")
print("2. Filtre de Prewitt")
print("3. Filtre de Canny")

while filtre_choice != 1 and filtre_choice != 2 and filtre_choice != 3:
    filtre_choice = input("Entrez le numéro du filtre à appliquer : ")
    if filtre_choice != "1" and filtre_choice != "2" and filtre_choice != "3":
        clear()
        print("Filtre invalide")
    else:
        filtre_choice = int(filtre_choice)


while rep != "y" and rep != "n":
    rep = input("Voulez-vous activer le mode benchmark ? (y/n) : ")
    if rep == "y":
        BENCHMARK = True
    elif rep == "n":
        BENCHMARK = False
    else:
        clear()
        print("Réponse invalide")

def demander_seuil(question):
    seuil = ""
    while not seuil.isnumeric() or (seuil.isnumeric() and not 0 <= float(seuil) <= 1):
        seuil = input(question)
        if not seuil.isnumeric() or (seuil.isnumeric() and not 0 <= float(seuil) <= 1):
            clear()
            print("Seuil invalide")
        else:
            return float(seuil)

if not BENCHMARK:
    if filtre_choice == 1:
        seuil_sobel = demander_seuil("Entrez le seuil pour le filtre de sobel (0.0 - 1.0) (0.0 -> pas de seuil) : ")
        sobelFilter(input_file, float(seuil_sobel)).save("output/"+input_file[:-4]+"_sobel_output.png")
    elif filtre_choice == 2:
        seuil_prewitt = demander_seuil("Entrez le seuil pour le filtre de prewitt (0.0 - 1.0) (0.0 -> pas de seuil) : ")
        prewittFilter(input_file, float(seuil_prewitt)).save("output/"+input_file[:-4]+"_prewitt_output.png")
    elif filtre_choice == 3:
        seuil_canny = demander_seuil("Entrez le seuil de canny (>0.0) (1.0 -> pas de seuil) : ")
        seuil_sobel = demander_seuil("Entrez le seuil du filtre de sobel (0.0 - 1.0) (0.0 -> pas de seuil) : ")
        canyFilter(input_file, float(seuil_canny), float(seuil_sobel)).save("output/"+input_file[:-4]+"_canny_output.png")
    print("Filtre appliqué avec succès. Vous trouverez le résultat dans le dossier output.")
    os.system("pause")        
else:
    if filtre_choice == 1:
        seuil = demander_seuil("Entrez le seuil de détection des contours (0.0 - 1.0) : ")
        elapsed_moy = 0
        execution_times[input_file] = []
        for j in range(1, 20):
            start = time.time()
            img = sobelFilter(input_file,seuil)
            end = time.time()
            elapsed = end - start
            execution_times[input_file].append(elapsed)
            elapsed_moy += elapsed
            print(j*"#" + (19-j)*" ", round((j/20)*100), "%", end="\r")
        elapsed_moy /= 10
        print(input_file+" ("+ str(Image.open(input_file).size[0]) + "x"+ str(Image.open(input_file).size[1]) +") temps moyen : ", round (elapsed_moy * 1000), "ms                      ")
    elif filtre_choice == 2:
        seuil = demander_seuil("Entrez le seuil de détection des contours (0.0 - 1.0) : ")
        elapsed_moy = 0
        execution_times[input_file] = []
        for j in range(1, 20):
            start = time.time()
            img = prewittFilter(input_file,seuil)
            end = time.time()
            elapsed = end - start
            execution_times[input_file].append(elapsed)
            elapsed_moy += elapsed
            print(j*"#" + (19-j)*" ", round((j/20)*100), "%", end="\r")
        elapsed_moy /= 10
        print(input_file+" ("+ str(Image.open(input_file).size[0]) + "x"+ str(Image.open(input_file).size[1]) +") temps moyen : ", round (elapsed_moy * 1000), "ms                      ")
    elif filtre_choice == 3:
        seuil = demander_seuil("Entrez le seuil de détection des contours (0.0 - 1.0) : ")
        comparaison = demander_seuil("Entrez la valeur de comparaison (0.0 - 1.0) : ")
        elapsed_moy = 0
        execution_times[input_file] = []
        for j in range(1, 20):
            start = time.time()
            img = canyFilter(input_file,seuil,comparaison)
            end = time.time()
            elapsed = end - start
            execution_times[input_file].append(elapsed)
            elapsed_moy += elapsed
            print(j*"#" + (19-j)*" ", round((j/20)*100), "%", end="\r")
        elapsed_moy /= 10
        print(input_file+" ("+ str(Image.open(input_file).size[0]) + "x"+ str(Image.open(input_file).size[1]) +") temps moyen : ", round (elapsed_moy * 1000), "ms                      ")


colors = ['red', 'blue', 'green', 'orange']


if BENCHMARK:
    
    # Création du graphique
    plt.figure(figsize=(10, 6))

    # Tracer les lignes pour chaque image
    for i, (image, times) in enumerate(execution_times.items()):
        # Placer les points et les lignes
        plt.plot(range(1, len(times) + 1), times, marker='o', color=colors[i], label=image)

    # Configurer les labels et le titre
    plt.xlabel('Essais')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Comparaison des temps d\'exécution pour différentes images')
    #plt.yscale('log')
    plt.xticks(range(1, len(next(iter(execution_times.values()))) + 1))

    # Ajouter la légende
    plt.legend()

    # Afficher le graphique
    plt.show()
