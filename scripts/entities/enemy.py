from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np

class Enemy(Entity):
    def __init__(self, *args, health=3, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array([100., 100.])
        self.speed = 2

        self.color = (255, 0, 0)
        self.active_color = self.color

        self.hit_flash_time = 0.1
        self.hit_flash_timer = 0.

    def update(self):
        #dir_to_player = utils.normalize(game.player.position - self.position)
        #self.velocity = dir_to_player * self.speed
        super().update()
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= self.game.deltatime
        else:
            self.active_color = self.color

    def damage(self, damage, source: DamageSource):
        super().damage(damage, source)
        self.hit_flash_timer = self.hit_flash_time
        self.active_color = (255, 255, 255)

    def render(self, offset = np.array([0, 0])):
        sprite = pygame.Surface(self.rect.size)
        sprite.fill(self.active_color)
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.rotate(sprite, np.rad2deg(np.atan2(self.velocity[1], self.velocity[0])))
        self.app.display.blit(sprite, self.pos - offset)
        super().update()
