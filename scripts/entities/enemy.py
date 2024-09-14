from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np

class Enemy(Entity):
    def __init__(self, *args, health=3, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array([100., 100.])
        self.speed = 2

        self.attack_distance = 15

        self.sprite.fill((255, 0, 0))

    def update(self):
        #dir_to_player = utils.normalize(game.player.pos - self.pos)
        #self.velocity = dir_to_player * self.speed
        super().update()
        self.hit_flash.update(self.app.deltatime)
        self.forward = utils.normalize(self.app.player.pos - self.pos)

    def damage(self, damage, source: DamageSource):
        super().damage(damage, source)

    def render(self, offset = np.array([0, 0])):
        sprite = super().render(offset)
        self.app.display.blit(sprite, self.pos - self.size * 0.5 - offset)
