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

float norm(vec2 img){
    return sqrt(img.r*img.r + img.g*img.g);
}


float isHigest(float x, float y, vec2 uv, float alpha){
    if (norm(texture(Texture, uv + vec2(x,y)).rg) < alpha*norm(texture(Texture, uv).rg) &&
    norm(texture(Texture, uv + vec2(-x,-y)).rg) < alpha*norm(texture(Texture, uv).rg)){
        return 1.;
    }else{
        return 0.;
    }
}




void main()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = v_texcoord;
    float influ = 1.;
    vec2 comparaison2;
    comparaison2 = comparaison;
    
    
    
    vec3 col;
    col = vec3(isHigest(texture(Texture, uv).r*influ/Resolution.x,texture(Texture, uv).g*influ/Resolution.y,uv,seuil));

    // Output to screen
    fragColor = vec4(col,0.);
}
