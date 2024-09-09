import pygame

import math
from scripts.const import *

from scripts.components.health import Health

class Projectile():
    def __init__(self,app,player,pos,size,direction,gravity=GRAV):

        self.app = app

        self.player = player

        self.pos = pos
        self.size = size

        self.gravity = gravity

        self.direction = direction

        self.startTime = self.app.deltatime

        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

        self.collision_rects = self.closest_tiles(self.app.tile_system.tiles)

        self.velocity = [0,0]

        self.velocity[0] += self.direction.x
        self.velocity[1] += self.direction.y

    def physics(self):
        self.velocity[1] = min(5,self.velocity[1] + self.gravity)

        frame_movement = [self.velocity[0],self.velocity[1]]

        # x stuff
        self.pos[0] += frame_movement[0]
        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])

        # y stuff
        self.pos[1] += frame_movement[1]
        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self):
        self.collision_rects = self.closest_tiles(self.app.tile_system.tiles)
        self.physics()

    def get_entity_collision(self):
        for entity in self.app.entities:
            if self == entity:
                continue
            if self.player == entity:
                continue
            if self.rect.colliderect(entity.rect):
                return entity
            
    def get_collision(self):

        collision = self.rect.collidelist(self.collision_rects)

        if collision == -1:
            return

        return self.collision_rects[collision]
            
    def closest_tiles(self,tiles):

        closest_tiles = []

        for tile in tiles:
            tile_dist = math.sqrt((self.pos[0]-tile["pos"][0])**2 + (self.pos[1]-tile["pos"][1])**2)
            if tile_dist < 64:
                closest_tiles.append(tile)

        closest_rects = [tile["rect"] for tile in closest_tiles]

        return closest_rects
        