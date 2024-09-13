from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np
from scripts.components.hitflash import HitFlash

class Enemy(Entity):
    def __init__(self, *args, health=3, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array([100., 100.])
        self.speed = 2

        self.hit_flash = HitFlash()

    def update(self):
        #dir_to_player = utils.normalize(game.player.pos - self.pos)
        #self.velocity = dir_to_player * self.speed
        super().update()
        self.hit_flash.update(self.app.deltatime)

    def damage(self, damage, source: DamageSource):
        self.hit_flash.begin()
        self.active_color = (255, 255, 255)
        super().damage(damage, source)

    def render(self, offset = np.array([0, 0])):
        sprite = pygame.Surface(self.rect.size)
        sprite.fill((255, 0, 0))

        sprite.fill(self.hit_flash.color_to_add, special_flags=pygame.BLEND_RGBA_ADD)

        sprite.set_colorkey((0, 0, 0))

        sprite = pygame.transform.rotate(sprite, np.rad2deg(np.atan2(self.velocity[1], self.velocity[0])))
        self.app.display.blit(sprite, self.pos - offset)
        super().render(offset)
