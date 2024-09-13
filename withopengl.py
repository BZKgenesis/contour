import numpy as np
from PIL import Image
import moderngl
import time

def sobelFilter(ImageName):
    # Charger l'image
    image = Image.open(ImageName).convert('RGB')
    image_data = np.array(image).astype('f4') / 255.0  # Normaliser les couleurs

    # Création du contexte OpenGL
    ctx = moderngl.create_standalone_context()

    # Création de la texture de l'image
    texture = ctx.texture(image.size, 3, (image_data * 255).astype('u1').tobytes())
    texture.build_mipmaps()

    # Créer un framebuffer pour le rendu de l'image avec le shader
    fbo = ctx.framebuffer(color_attachments=[ctx.texture(image.size, 3)])
    fbo.use()

    with open ("edgeDetection.frag", "r") as myfile:
        data = myfile.read()

    # Création du programme (vertex + fragment shaders)
    prog = ctx.program(
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

    prog['Resolution'] = (image.size[0], image.size[1])
    prog['MousePos'] = (image.size[0], 0)

    # Définit la géométrie du rectangle à rendre (un quadrilatère couvrant tout l'écran)
    vertices = np.array([
        # Positions    # Coordonnées de texture
        -1.0,  1.0,    0.0, 1.0,
        -1.0, -1.0,    0.0, 0.0,
        1.0,  1.0,    1.0, 1.0,
        1.0, -1.0,    1.0, 0.0,
    ], dtype='f4')

    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_texcoord')

    # Utilisation de la texture et rendu
    texture.use()
    vao.render(moderngl.TRIANGLE_STRIP)

    # Récupérer les données de l'image du framebuffer
    data = fbo.read(components=3)
    output_image = Image.frombytes('RGB', image.size, data)

    # Enregistrer l'image
    return output_image



start = time.time()
img = sobelFilter("1.png")
end = time.time()
elapsed = end - start
img.show()
print("img 1 : ", elapsed)