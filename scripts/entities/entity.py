import pygame

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
        collision = self.collision()
        if collision:
            if frame_movement[0] > 0:
                self.rect.right = self.collidables[collision].left
            if frame_movement[0] < 0:
                self.rect.left = self.collidables[collision].right
            self.pos[0] = self.rect.x

        self.pos[1] += frame_movement[1]
        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])
        collision = self.collision()

        if collision:
            if frame_movement[1] > 0:
                self.rect.bottom = self.collidables[collision].top
            if frame_movement[1] < 0:
                self.rect.top = self.collidables[collision].bottom
            self.pos[1] = self.rect.y


    def get_collisions(self):
        self.collidables = []

        for tile in self.app.tile_system.tiles:
            if pygame.Vector2(tile["pos"][0],tile["pos"][1]).distance_to(self.pos) < 32:
                rect = pygame.Rect(tile["pos"][0],tile["pos"][1],tile["size"][0],tile["size"][1])
                self.collidables.append(rect)

    def collision(self):
        collision = self.rect.collidelist(self.collidables)

        if collision == -1:
            return False

        return collision

    def update(self):
        self.get_collisions()

        self.move()

    def render(self):
        
        rect = self.rect

        self.display_pos[0] += (self.pos[0] - self.display_pos[0]) / 10
        self.display_pos[1] += (self.pos[1] - self.display_pos[1]) / 10
        
        rect.x = self.display_pos[0]
        rect.y = self.display_pos[1]

        pygame.draw.rect(self.app.display,(0,0,0),self.rect)