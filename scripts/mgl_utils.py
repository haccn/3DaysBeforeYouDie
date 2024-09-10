import pygame

import random

import moderngl

import array

import noise




def load_program(ctx,program_name):

    with open(f'shaders/{program_name}.vert') as file:
        vertex_shader = file.read()

    with open(f'shaders/{program_name}.frag') as file:
        fragment_shader = file.read()

    program = ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)

    return program

def surf_to_texture(ctx,surf):
    tex = ctx.texture(surf.get_size(),4)
    tex.filter = (moderngl.NEAREST,moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

def render_object(ctx,program,quad_buffer):
    return ctx.vertex_array(program,[(quad_buffer,'2f 2f','vert','texcoord')])

def get_noise(scale,seed=random.randrange(1,100),mult=1):
    noise_surf = pygame.Surface(scale)

    noise_array = []
    
    for x in range(scale[0]):
        for y in range(scale[1]):
            v = noise.pnoise2(x / (scale[0] / mult), y / (scale[1] / mult),octaves=2,base=seed)
            v += .5 * noise.pnoise2(x / (scale[0] / mult), y / (scale[1] / mult),octaves=8,base=seed)
            v += .25 * noise.pnoise2(x / (scale[0] / mult), y / (scale[1] / mult),octaves=16,base=seed)
            v += .125 * noise.pnoise2(x / (scale[0] / mult), y / (scale[1] / mult),octaves=32,base=seed)
            v = (v + 1) / 2

            noise_array.append(-v * 5)
            noise_surf.set_at((x, y), (max(0,min(255,(v * 255))),max(0,min(255,(v * 255))),max(0,min(255,(v * 255)))))

    pygame.image.save(noise_surf,"assets/noise/noise.png")
    #noise_img = pygame.image.save(noise_surf,"assets/noise/noise.png")

    return noise_surf