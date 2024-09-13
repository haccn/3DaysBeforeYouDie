import pygame
import numpy as np

class Rigidbody:
    def __init__(self,
        app,
        pos = np.array([0., 0.]),
        size = np.array([20., 20.]),
        velocity = np.array([0., 0.]),
        static_friction = 0.5,
        kinetic_friction = 3,
        forward = np.array([0., -1.]),
     ):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.velocity = velocity
        self.static_friction = static_friction
        self.kinetic_friction = kinetic_friction
        self.forward = forward

    def update(self, deltatime):
        # collect relevant collidables

        collidables = []
        collidable_max_distance = 40

        # filter out distant tiles
        for tile in self.app.tile_system.tiles:
            if np.linalg.norm(tile["rect"].center - self.pos) < collidable_max_distance:
                collidables.append(tile["rect"])

        for enemy in self.app.enemies:
            if np.linalg.norm(enemy.pos - self.pos) < collidable_max_distance and\
                enemy != self:
                collidables.append(enemy.rect)

        if self.app.player != self:
            collidables.append(self.app.player.rect)

        # TODO add other entities to collidables

        # update position and handle collisions

        prevx = self.pos[0]
        self.pos[0] += self.velocity[0] * deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            self.pos[0] = prevx

        prevy = self.pos[1]
        self.pos[1] += self.velocity[1] * deltatime
        collision = pygame.Rect(self.pos, self.size).collidelist(collidables)
        if collision != -1:
            self.pos[1] = prevy

        self.rect.update(self.pos, self.size)

        # apply friction

        if (np.abs(self.velocity) < self.static_friction).all():
            self.velocity = np.zeros(2)
        else:
            self.velocity -= self.velocity * self.kinetic_friction * deltatime
