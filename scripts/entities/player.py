import pygame

from scripts.entities.entity import Entity
from scripts.utils import *

class Player(Entity):
    def __init__(self,app,pos,size,health):
        super().__init__(app, pos, size,health)

        self.resources = {"money" : 0}
        self.modes = ["Fighting","Building"]
        self.mode = "Fighting"

    def input(self):
        for event in self.app.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.movement[2] = True
                if event.key == pygame.K_s:
                    self.movement[3] = True
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
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
                    self.app.building_system.place()

                #print(self.mode)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movement[2] = False
                if event.key == pygame.K_s:
                    self.movement[3] = False
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False

    
    def update(self):
        self.input()
        return super().update()
    
    def render(self,offset=(0,0)):
        if self.mode == "Building":
            self.app.building_system.preview()
        self.app.display.blit(pygame.transform.scale(load_img("player/player.png"),self.size),(self.pos[0]-offset[0],self.pos[1]-offset[1]))
