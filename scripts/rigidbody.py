import pygame
import numpy as np

class Rigidbody:
    def __init__(self,
        pos = np.array([0., 0.]),
        size = (20., 20.),
        velocity = np.array([0., 0.]),
        static_friction = 0.5,
        kinetic_friction = 3,
        forward = np.array([0., -1.]),
     ):
        self.pos = pos
        self.rect = pygame.Rect(pos, size)
        self.velocity = velocity
        self.static_friction = static_friction
        self.kinetic_friction = kinetic_friction
        self.forward = forward

    def update(self, deltatime):
        self.position += self.velocity * deltatime
        self.rect.center = self.pos
        if (np.abs(self.velocity) < self.static_friction).all():
            self.velocity = np.zeros(2)
        else:
            self.velocity -= self.velocity * self.kinetic_friction * deltatime
