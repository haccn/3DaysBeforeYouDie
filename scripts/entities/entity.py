import pygame

import math

import numpy as np

from scripts.components.health import Health
from scripts.rigidbody import Rigidbody
from scripts.utils import *

class Entity(Rigidbody):
    def __init__(self,app,health,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.app = app
        self.health = Health(self.app,health)

    def update(self):
        super().update(self.app.deltatime)

    def render(self,offset=(0,0)):
        pass
