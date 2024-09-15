import numpy as np
from PIL import Image
import moderngl
import time
import matplotlib.pyplot as plt

COMPARAISONX = 1. # Séparation de l'image pour pouvoir comparer avec et sans le filtre (0.0 - 1.0)
SEUIL = 0. # Seuil de détection des contours (0.0 - 1.0)
BENCHMARK = True # Passer en mode mesure de performance (True) ou en mode rendu (False)

# Création du contexte OpenGL
ctx = moderngl.create_standalone_context()
print("Vendor:", ctx.info['GL_VENDOR'])
print("Renderer:", ctx.info['GL_RENDERER'])
print("Version:", ctx.info['GL_VERSION'])
#print("Shading Language Version:", ctx.info['GL_SHADING_LANGUAGE_VERSION'])

def OpenGlEnv(ImageName, fragmentShaderData):
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
    prog['comparaison'] = (COMPARAISONX, 0)  # on passe les paramètres dans le shader
    prog['seuil'] = SEUIL 

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

def sobelFilter(ImageName):
    
    with open ("sobelFilter.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    return OpenGlEnv(ImageName, data) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader


def differenceGaussian(ImageName):
    
    with open ("differenceGauss.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()
    return OpenGlEnv(ImageName, data) # on appelle la fonction OpenGlEnv avec le nom de l'image et le shader

    
execution_times = {}

for i in range(1, 5):
    if BENCHMARK:
        elapsed_moy = 0
        execution_times["Image "+str(i)] = []
        for j in range(1, 20):
            start = time.time()
            img = sobelFilter(str(i)+".png")
            end = time.time()
            elapsed = end - start
            execution_times["Image "+str(i)].append(elapsed)
            elapsed_moy += elapsed
        elapsed_moy /= 10
        print("img "+str(i)+" : ", round (elapsed_moy * 1000), "ms")
    else:
        sobelFilter(str(i)+".png").save("output\\output"+str(i)+".png")

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
    plt.yscale('log')
    plt.xticks(range(1, len(next(iter(execution_times.values()))) + 1), [f'{i}' for i in range(1, len(next(iter(execution_times.values()))) + 1)])

    # Ajouter la légende
    plt.legend()

    # Afficher le graphique
    plt.show()

"""
specs:
CPU:i5-12450H
RAM:8,00 Go
GPU: Intel(R) UHD Graphics


perfs:
img 1 :  55 ms 
img 2 :  31 ms
img 3 :  75 ms
img 4 :  1212 ms (1s 212 ms)
"""