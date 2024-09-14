import pygame

import sys

from scripts.mouse import Mouse
from scripts.const import *
from level_creator_scripts.tile_system import tile_system

class main():

    def __init__(self):
        self.display = pygame.Surface(DISPLAY_SIZE)
        self.screen = pygame.display.set_mode(WIN_SIZE)

        pygame.mouse.set_visible(False)

        # clock stuff

        self.clock = pygame.time.Clock()

        self.deltatime = 0

        self.delta = 0

        #mouse

        self.mouse = Mouse(self,(0,0),(16,16))

        # tile system

        self.tile_system = tile_system(self)

        self.all_events = self.events()



    def events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        return events



    def update(self):
        while True:

            #updates

            self.all_events = self.events()

            self.tile_system.update()

            self.mouse.update()

            if self.mouse.click():
                self.tile_system.add_tile(self.mouse.pos,self.tile_system.tile_types[self.tile_system.tile_type])

            if self.mouse.right_click():
                self.tile_system.remove_tile(self.mouse.pos)

            self.deltatime += self.clock.tick(60) / 1000
            self.delta = self.clock.get_fps() / 1000

            #render

            self.render()


    def render(self):
        self.display.fill((255,255,255))

        #self.mouse.render()


        self.tile_system.render()

        self.tile_system.tile_preview(self.mouse.pos)

        self.screen.blit(pygame.transform.scale(self.display,WIN_SIZE),(0,0))

        pygame.display.update()


main().update()
