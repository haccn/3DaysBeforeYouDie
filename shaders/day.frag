#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

vec4 day_color = vec4(1.0,1.0,1.0,1.0);

vec4 night_color = vec4(.28/2,.27/2,.6/2,1.0);

void main() {

    vec3 time_color = vec3(day_color.r * (1 - time) + night_color.r * time,
        day_color.g * (1 - time) + night_color.g * time,day_color.b * (1 - time) + night_color.b * time);
    
    f_color = vec4(texture(tex,uvs).rgb * time_color.rgb,1.0);


}
