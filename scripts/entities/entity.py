import pygame

import math

import numpy as np

from scripts.components.health import Health
from scripts.rigidbody import Rigidbody
from scripts.utils import *

class DamageSource:
    def __init__(self, point):
        self.point = point

class Entity(Rigidbody):
    def __init__(self,app,health,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.app = app
        self.health = Health(self.app,health)
        self.recoil_speed = 200.

    def update(self):
        super().update(self.app.deltatime)

    def damage(self, damage, source: DamageSource):
        self.health.takeDamage(damage)
        self.velocity = normalize(self.position - source.point) * self.recoil_speed
        # TODO do something when health is 0
        # this will need to be handled differently by the player and the enemies
        #if self.health == 0:
        #    del self

    def render(self,offset=np.array([0, 0])):
        pass
