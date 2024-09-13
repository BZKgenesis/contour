#version 330 core

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

float difference(float X, float Y, vec2 uv){
    return abs(texture(iChannel0,uv + vec2(X,Y)) - texture(iChannel0,uv  - vec2(X,Y))).r + 
        abs(texture(iChannel0,uv + vec2(X,Y)) - texture(iChannel0,uv  - vec2(X,Y))).g + 
        abs(texture(iChannel0,uv  + vec2(X,Y)) - texture(iChannel0,uv  - vec2(X,Y))).b;

}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;
    
    float seuil = 0.55;
    vec3 col;
    // Time varying pixel color
    
    float pixelX = 1./iResolution.x;
    float pixelY = 1./iResolution.y;

    float value = difference(pixelX,0.,uv) + difference(0.,pixelY,uv) + difference(pixelX,pixelY,uv) + difference(-pixelX,pixelY,uv);
    
    col = vec3(clamp(map(value, 0.,1., -0.5,2.),0.,1.));
    
    
    

    // Output to screen
    fragColor = vec4(col,1.0);
}