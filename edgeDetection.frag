#version 330

uniform sampler2D Texture;
in vec2 v_texcoord;
uniform vec2 Resolution;
uniform vec2 MousePos;
out vec4 fragColor;

float getValue(vec2 pos){
    return (texture(Texture, pos).r + texture(Texture, pos).g + texture(Texture, pos).b)/3.;

}

float sobelX(float x, float y, vec2 uv){
    return -2.*getValue(uv + vec2(-x,0.)) + -getValue(uv + vec2(-x,y)) + -getValue(uv - vec2(-x,-y)) + 
    2.*getValue(uv + vec2(x,0.)) + getValue(uv + vec2(x,y)) + getValue(uv - vec2(x,-y));
}

float sobelY(float x, float y, vec2 uv){
    return -2.*getValue(uv + vec2(0.,y)) + -getValue(uv + vec2(x,y)) + -getValue(uv - vec2(-x,y)) + 
    2.*getValue(uv + vec2(0.,-y)) + getValue(uv + vec2(x,-y)) + getValue(uv - vec2(-x,-y));
}


void main()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = v_texcoord;

    float pixelX = 1./Resolution.x;
    float pixelY = 1./Resolution.y;
    float seuil = 0.05;

    // Time varying pixel color
    float sobelXVal = abs(sobelX(pixelX,pixelY,uv));
    float sobelYVal = abs(sobelY(pixelX,pixelY,uv));
    vec3 col;
    

    if (v_texcoord.x < MousePos.x){
        if (sqrt(sobelXVal*sobelXVal + sobelYVal*sobelYVal)> seuil){
            col = vec3(sobelXVal,sobelYVal,0.);
        }else
        {
            col = vec3(0.);
        }
    }else{
        col = texture(Texture, uv).rgb;
    }


    // Output to screen
    fragColor = vec4(col,1.0);
}