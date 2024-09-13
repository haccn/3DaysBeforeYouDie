import pygame

import numpy as np

from scripts.entities.entity import Entity
from scripts.utils import *

class Player(Entity):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.speed = 100.
        self.resources = {"money" : 0}
        self.modes = ["Fighting","Building"]
        self.mode = "Fighting"

    def input(self):
        for event in self.app.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    next_mode = self.modes.index(self.mode) + 1
                    if next_mode >= len(self.modes):
                        next_mode = 0
                    self.mode = self.modes[next_mode]
                if self.mode == "Building":
                    if event.key == pygame.K_q:
                        self.app.building_system.placement = max(0,self.app.building_system.placement - 1)
                    if event.key == pygame.K_e:
                        self.app.building_system.placement = min(len(self.app.building_system.building_types) - 1,self.app.building_system.placement + 1)
            if self.mode == "Building":
                if self.app.mouse.click():
                    print("Yes")
                    self.app.building_system.place_building()

                #print(self.mode)


    def update(self):
        self.input()
        input_vec = normalize(np.array([
            float(self.app.keys_pressed[pygame.K_d] | self.app.keys_pressed[pygame.K_RIGHT]) -
                float(self.app.keys_pressed[pygame.K_a] | self.app.keys_pressed[pygame.K_LEFT]),
            float(self.app.keys_pressed[pygame.K_s] | self.app.keys_pressed[pygame.K_DOWN]) -
                float(self.app.keys_pressed[pygame.K_w] | self.app.keys_pressed[pygame.K_UP]),
        ]))
        self.velocity = input_vec * self.speed
        super().update()

    def render(self,offset=(0,0)):
        if self.mode == "Building":
            self.app.building_system.preview()
        self.app.display.blit(pygame.transform.scale(load_img("player/player.png"),self.size),(self.pos[0]-offset[0],self.pos[1]-offset[1]))
        super().render(offset)
