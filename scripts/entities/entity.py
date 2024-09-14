import pygame
import math
import numpy as np
from scripts.rigidbody import Rigidbody
from scripts.utils import *
from scripts.components.hitflash import HitFlash

class DamageSource:
    def __init__(self, point):
        self.point = point

class Entity(Rigidbody):
    def __init__(self,
        app,
        health = 3,
        attack_distance = 30.,
        attack_damage = 1,
        forward = [0., -1.],
        recoil_speed = 200.,
        sprite = None,
        **kwargs,
    ):
        super().__init__(app, **kwargs)

        self.health = health
        self.hit_flash = HitFlash()

        self.attack_distance = attack_distance
        self.attack_damage = attack_damage
        self.forward = np.array(forward)

        self.recoil_speed = recoil_speed

        self.sprite = pygame.Surface(self.size) if sprite is None else sprite

    def update(self):
        self.hit_flash.update(self.app.deltatime)
        super().update()

    def damage(self, damage: int, source: DamageSource):
        self.health -= damage
        self.velocity = normalize(self.pos - source.point) * self.recoil_speed
        self.hit_flash.begin()
        # TODO do something when health is 0
        # this will need to be handled differently by the player and the enemies
        #if self.health == 0:
        #    del self

    def render(self,offset=[0, 0]) -> pygame.Surface:
        offset = np.array(offset)
        # FOR DEBUGGING RAYCASTING
        hits = raycast(Ray(self.pos, self.pos + self.forward * self.attack_distance), self.app.enemies + [self.app.player])
        color = (0, 255, 0) if len(hits) > 0 else (128, 128, 128)
        pygame.draw.line(self.app.display, color, self.pos - offset, self.pos + self.forward * self.attack_distance - offset)
        for hit in hits:
            pygame.draw.circle(self.app.display, (0, 255, 0), hit.point - offset, 3)

        sprite = self.sprite.copy()
        sprite.fill(self.hit_flash.color_to_add, special_flags=pygame.BLEND_RGBA_ADD)
        return sprite
