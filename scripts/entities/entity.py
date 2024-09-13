import pygame

import math

from scripts.components.health import Health
from scripts.utils import *

class Entity():
    def __init__(self,app,pos,size,health):
        self.app = app

        self.pos = list(pos)
        self.display_pos = self.pos
        self.size = size

        self.rect = pygame.Rect(self.pos[0],self.size[1],self.size[0],self.size[1])

        self.lerp_time = 0

        self.health = Health(self.app,health)

        self.collidables = []

        self.velocity = [0,0]
        self.movement = [False,False,False,False]

    def move(self):
        frame_movement = [self.velocity[0] + (self.movement[1] - self.movement[0]),self.velocity[1] + (self.movement[3] - self.movement[2])]

        self.pos[0] += frame_movement[0]
        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])
        collision = self.rect.collidelist(self.collidables)

        
        if collision != -1:
            if frame_movement[0] > 0:
                self.rect.right = self.collidables[collision].left
            if frame_movement[0] < 0:
                self.rect.left = self.collidables[collision].right
            self.pos[0] = self.rect.x

        self.pos[1] += frame_movement[1]
        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])
        collision = self.rect.collidelist(self.collidables)

        if collision != -1:
            if frame_movement[1] > 0:
                self.rect.bottom = self.collidables[collision].top
            if frame_movement[1] < 0:
                self.rect.top = self.collidables[collision].bottom
            self.pos[1] = self.rect.y


    def get_collisions(self):
        closest_tiles = []

        for tile in self.app.tile_system.tiles:
            tile_dist = math.sqrt((self.pos[0]-tile["pos"][0])**2 + (self.pos[1]-tile["pos"][1])**2)
            if tile_dist < 96:
                closest_tiles.append(tile)


        closest_rects = [tile["rect"] for tile in closest_tiles]

        return closest_rects

    def update(self):
        self.collidables = self.get_collisions()

        self.move()

    def render(self,offset=(0,0)):
        self.app.display.blit(pygame.transform.scale(load_img("player/player.png"),self.size),(self.pos[0]-offset[0],self.pos[1]-offset[1]))