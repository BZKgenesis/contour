import numpy as np
from PIL import Image
import moderngl
import time

COMPARAISONX = 0.5 # Séparation de l'image pour pouvoir comparer avec et sans le filtre (0.0 - 1.0)
SEUIL = 0.55 # Seuil de détection des contours (0.0 - 1.0)

def sobelFilter(ImageName):
    # Charger l'image
    image = Image.open(ImageName).convert('RGB') # on ouvre l'image et on la converti en RGB (pour supprimer le canal alpha si il existe)
    image_data = np.array(image).astype('f4') / 255.0  # Normaliser les couleurs (0.0 - 1.0)
    # f4 : float 32 bits

    # Création du contexte OpenGL
    ctx = moderngl.create_standalone_context()  

    # Création de la texture de l'image
    texture = ctx.texture(image.size, 3, (image_data * 255).astype('u1').tobytes()) # on reprend l'image convertie en RGB et on la converti en 8 bits
    #u1 : unsigned int 8 bits (0 - 255)

    texture.build_mipmaps() # Générer les mipmaps pour le filtrage (sa sert a rien dans notre cas)

    # Créer un framebuffer pour le rendu de l'image avec le shader
    fbo = ctx.framebuffer(color_attachments=[ctx.texture(image.size, 3)]) # on crée un framebuffer avec une texture de la taille de l'image
    fbo.use() # on utilise le framebuffer
    # fbo : framebuffer object (objet qui contient les textures de rendu)


    with open ("sobelFilter.frag", "r") as myfile: # on ouvre le fichier contenant le shader (il est dans un fichier séparé pour plus de lisibilité)
        #'r' : read (lecture seule)
        data = myfile.read()

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
        fragment_shader=data
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


for i in range(1, 5):
    start = time.time()
    img = sobelFilter(str(i)+".png")
    end = time.time()
    elapsed = end - start
    print("img "+str(i)+" : ", round (elapsed * 1000), "ms")
    img.save("output\\output"+str(i)+".png")