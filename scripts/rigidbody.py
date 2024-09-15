import pygame
import numpy as np

class Rigidbody:
    def __init__(self,
        app,
        pos = [0., 0.],
        size = [10., 10.],
        acceleration = [0., 0.],
        velocity = [0., 0.],
        static_friction = 0.5,
        kinetic_friction = 4.,
     ):
        self.app = app

        self.pos = np.array(pos)
        self.size = np.array(size)
        self.rect = pygame.Rect(pos, size)

        self.acceleration = np.array(acceleration)
        self.velocity = np.array(velocity)
        self.static_friction = static_friction
        self.kinetic_friction = kinetic_friction

    def update(self):
        # collect relevant collidables

        collidables = []
        collidable_max_distance = 40.

        # filter out distant tiles
        for collidable in self.app.collidables:
            if np.linalg.norm(collidable.center - self.pos) < collidable_max_distance:
                collidables.append(collidable)

        for enemy in self.app.enemies:
            if np.linalg.norm(enemy.pos - self.pos) < collidable_max_distance and enemy != self:
                collidables.append(enemy.rect)

        if self.app.player != self:
            collidables.append(self.app.player.rect)

        # update position and handle collisions

        self.velocity += self.acceleration * self.app.deltatime

        prevx = self.pos[0]
        self.pos[0] += self.velocity[0] * self.app.deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            if self.velocity[0] > 0:
                self.rect.right = collidables[collision].left
            if self.velocity[0] < 0:
                self.rect.left = collidables[collision].right
            self.pos[0] = self.rect.x

        self.pos[1] += self.velocity[1] * self.app.deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            if self.velocity[1] > 0:
                self.rect.bottom = collidables[collision].top
                self.velocity[1] = 0
            if self.velocity[1] < 0:
                self.rect.top = collidables[collision].bottom
            self.pos[1] = self.rect.y

        self.rect.update(self.pos,self.size)
        self.rect.size = self.size

        # apply friction

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
