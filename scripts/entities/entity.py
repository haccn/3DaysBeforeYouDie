import pygame

import math

import numpy as np

from scripts.rigidbody import Rigidbody
from scripts.utils import *

class DamageSource:
    def __init__(self, point):
        self.point = point

class Entity(Rigidbody):
    def __init__(self,app,health,*args,forward = np.array([0., -1.]),**kwargs):
        super().__init__(app,*args,**kwargs)

        self.health = 3

        self.forward = forward

        self.recoil_speed = 200.

    def update(self):
        super().update()
        if (self.velocity != 0.).any():
            self.forward = normalize(self.velocity)

    def damage(self, damage, source: DamageSource):
        self.health -= damage
        self.velocity = normalize(self.pos - source.point) * self.recoil_speed
        # TODO do something when health is 0
        # this will need to be handled differently by the player and the enemies
        #if self.health == 0:
        #    del self

    def render(self,offset=np.array([0, 0])):
        pass
