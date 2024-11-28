#version 330

uniform sampler2D Texture; // uniform : variable qui ne change pas entre les différents pixels
// sampler2D : type de variable qui contient une texture 2D ainsi que la méthode pour la lire et l'afficher
in vec2 v_texcoord; // in : variable qui change entre les différents pixels c'est une variable d'entré (coordonnées de texture)
// vec2 : type de variable qui contient deux float (x et y)
uniform vec2 Resolution; 
uniform vec2 comparaison;
uniform float seuil;
out vec4 fragColor; // out : variable qui change entre les différents pixels c'est une variable de sortie (couleur du pixel) (c'est le résultat de notre shader)
// vec4 : type de variable qui contient 4 float (r,g,b,a) (rouge, vert, bleu, opacité)

float getValue(vec2 pos){ // fonction qui retourne la valeur d'un pixel de la texture à la position pos en niveau de gris
    // paramètres :
    // pos : coordonnées du pixel
    return (texture(Texture, pos).r + texture(Texture, pos).g + texture(Texture, pos).b)/3.; // on retourne la moyenne des trois composantes de couleur
}


// On sépare le filtre de sobel en deux fonctions pour pouvoir les appliquer séparément et avoir les coordonnées des gradients en x et en y
float sobelX(float x, float y, vec2 uv){ // fonction qui retourne la valeur du filtre de sobel en x
    // matrice de convolution pour le filtre de sobel
    // -1  0  1
    // -2  0  2
    // -1  0  1

    // paramètres :
    // x : taille d'un pixel en x
    // y : taille d'un pixel en y
    // uv : coordonnées du pixel
    return    -getValue(uv + vec2(-x, y))  +  0  +    getValue(uv + vec2( x, y)) + 
            -getValue(uv + vec2(-x,0.))  +  0  +  getValue(uv + vec2( x,0.)) +
              -getValue(uv + vec2(-x,-y))  +  0  +    getValue(uv + vec2( x,-y));
}

float sobelY(float x, float y, vec2 uv){ // fonction qui retourne la valeur du filtre de sobel en y
    // matrice de convolution pour le filtre de sobel
    // -1 -2 -1
    //  0  0  0
    //  1  2  1

    // paramètres :
    // x : taille d'un pixel en x
    // y : taille d'un pixel en y
    // uv : coordonnées du pixel
    return   -getValue(uv + vec2(-x, y))  + -getValue(uv + vec2(0., y))  + -getValue(uv + vec2( x, y)) + 
                 0                        +       0                        +     0                       +
              getValue(uv + vec2(-x,-y))  +  getValue(uv + vec2(0.,-y))  +  getValue(uv + vec2( x,-y));
}


void main()
{
    // On normalise les coordonné de pixel (0.0 - 1.0)
    vec2 uv = v_texcoord; // on change simplement de nom pour plus de clarté

    float pixelX = 1./Resolution.x; // on calcule la taille d'un pixel en x
    float pixelY = 1./Resolution.y; // on calcule la taille d'un pixel en y

    float sobelXVal = abs(sobelX(pixelX,pixelY,uv)); // on calcule la valeur du filtre de sobel en x
    float sobelYVal = abs(sobelY(pixelX,pixelY,uv)); // on calcule la valeur du filtre de sobel en y
    vec3 col; // on initialise la couleur du pixel
    

    if (v_texcoord.x < comparaison.x){ // si on est dans la première partie de l'image
        if (sqrt(sobelXVal*sobelXVal + sobelYVal*sobelYVal)> seuil){ // si la norme (√(x²+y²)) du gradient est supérieur à un seuil 
            col = vec3(sobelXVal,sobelYVal,0.); // on affiche le gradient
        }else
        {
            col = vec3(0.); // sinon on affiche du noir
        }
    }else{
        col = texture(Texture, uv).rgb; // sinon on affiche la texture
    }


    // On retourne la couleur du pixel
    fragColor = vec4(col,1.0); // on met l'opacité à 1
}