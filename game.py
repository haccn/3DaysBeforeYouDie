import math

import sys

import pygame

import moderngl

import array

from scripts.const import *
from scripts.mgl_utils import *
from scripts.utils import *
from scripts.mouse import Mouse
from level_creator_scripts.tile_system import tile_system
from scripts.entities.player import Player
from scripts.time_cycle import time_cycle
from scripts.building_system import Building_System

class game():
    def __init__(self) -> None:
        pygame.init()
        self.screen_size = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode((WIN_SIZE),pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.display = pygame.Surface(DISPLAY_SIZE)

        # clock

        self.all_events = self.events()

        self.clock = pygame.time.Clock()

        self.time_elapsed = 0
        self.deltatime = 0

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

        self.offset = [0,0]

        # mouse

        self.mouse = Mouse(self,(0,0),(16,16))

        #tile_system

        self.tile_system = tile_system(self)

        self.tile_system.loadsave("tileset_0")

        #player

        self.player = Player(app=self,size=(9,16),health=5)

        #self.time_cycle = time_cycle(self)

        self.building_system = Building_System(self)




    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #print(pygame.display.get_window_size())

        return events

    def update(self):
        while True:
            self.keys_pressed = pygame.key.get_pressed()
            self.all_events = self.events()

            self.render()

            self.player.update()

            self.mouse.update()

            self.building_system.update()

            self.deltatime = self.clock.tick() / 1000.
            self.time_elapsed += self.deltatime


    def render(self):
        self.display.fill((255,255,255))

        self.screen_size = pygame.display.get_window_size()
        self.display = pygame.transform.scale(self.display,(self.screen_size[0] / 2,self.screen_size[1] / 2))

        self.offset[0] += (self.player.rect.centerx - self.display.get_width() / 2 - self.offset[0]) / 15
        self.offset[1] += (self.player.rect.centery - self.display.get_height() / 2 - self.offset[1]) / 15

        #self.mouse.render()

        self.player.render(self.offset)

        self.tile_system.render(self.offset)

        self.building_system.render(self.offset)

        frame_tex = surf_to_texture(self.ctx,self.display)
        frame_tex.use(0)
        self.program['tex'] = 0


        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        #self.time_cycle.render()

        self.display.fill((255,255,255))

        self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))

        #self.time_cycle.render()

        pygame.display.flip()



if __name__ == "__main__":
    game().update()
