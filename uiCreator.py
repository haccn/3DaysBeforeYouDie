import sys

import pygame 

import moderngl

import array

from scripts.const import *
from scripts.mgl_utils import *

class uiCreator():
    def __init__(self) -> None:
        pygame.init()
        self.screen_size = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode((WIN_SIZE),pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.display = pygame.Surface(DISPLAY_SIZE)

        # clock 

        self.all_events = self.events()
        
        self.clock = pygame.time.Clock()

        # moderngl stuff

        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array.array ('f',[
        -1.0, 1.0, 0.0, 0.0,
        1.0, 1.0, 1.0, 0.0,
        -1.0,-1.0, 0.0, 1.0,
        1.0, -1.0, 1.0, 1.0
        ]))

        self.program = load_program(self.ctx,"default")

        self.render_object = render_object(self.ctx,self.program,self.quad_buffer)

        #mouse

        self.mouse = Mouse()
        
    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        return events

    def update(self):
        while True:
            self.events()

            self.render()


            
    def render(self):

        
        frame_tex = surf_to_texture(self.ctx,self.display)
        frame_tex.use(0)
        self.program['tex'] = 0

        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        self.display.fill((255,255,255))

        self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))

        pygame.display.flip()

if __name__ == "__main__":
    uiCreator().update()