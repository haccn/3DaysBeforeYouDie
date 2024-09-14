import pygame
import numpy as np

class Rigidbody:
    def __init__(self,
        app,
        pos = [0., 0.],
        size = [10., 10.],
        velocity = [0., 0.],
        static_friction = 0.5,
        kinetic_friction = 3.,
     ):
        self.app = app

        self.pos = np.array(pos)
        self.size = np.array(size)
        self.rect = pygame.Rect(pos, size)

        self.velocity = np.array(velocity)
        self.static_friction = static_friction
        self.kinetic_friction = kinetic_friction

    def update(self):
        # collect relevant collidables

        collidables = []
        collidable_max_distance = 40.

        # filter out distant tiles
        for tile in self.app.tile_system.tiles:
            if np.linalg.norm(tile["rect"].center - self.pos) < collidable_max_distance:
                collidables.append(tile["rect"])

        for enemy in self.app.enemies:
            if np.linalg.norm(enemy.pos - self.pos) < collidable_max_distance and enemy != self:
                collidables.append(enemy.rect)

        if self.app.player != self:
            collidables.append(self.app.player.rect)

        # update position and handle collisions

        prevx = self.pos[0]
        self.pos[0] += self.velocity[0] * self.app.deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            self.pos[0] = prevx

        prevy = self.pos[1]
        self.pos[1] += self.velocity[1] * self.app.deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            self.pos[1] = prevy

        self.rect.center = self.pos
        self.rect.size = self.size

        # apply friction

        print(self, " ", self.velocity)

        if abs(self.velocity[0]) < self.static_friction:
            self.velocity[0] = 0
        else:
            self.velocity[0] -= self.velocity[0] * self.kinetic_friction * self.app.deltatime

        if abs(self.velocity[1]) < self.static_friction:
            self.velocity[1] = 0
        else:
            self.velocity[1] -= self.velocity[1] * self.kinetic_friction * self.app.deltatime

        #if (np.abs(self.velocity) < self.static_friction).all():
        #    self.velocity = np.zeros(2)
        #else:
        #    self.velocity -= self.velocity * self.kinetic_friction * self.app.deltatime
