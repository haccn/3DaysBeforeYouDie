from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np

class Enemy(Entity):
    def __init__(self, *args, health=3, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array([100., 100.])
        self.speed = 2

        self.attack_distance = 12

        self.attack_damage = 1
        self.attack_cooldown = 3.
        self.attack_cooldown_timer = 0

        self.sprite.fill((255, 0, 0))

    def update(self):
        #dir_to_player = utils.normalize(self.app.player.pos - self.pos)
        #self.velocity = dir_to_player * self.speed

        self.forward = utils.normalize(self.app.player.pos - self.pos)

        if self.attack_cooldown_timer <= 0:
            hits = utils.raycast(utils.Ray(self.pos, self.pos + self.forward * self.attack_distance), [self.app.player])
            for hit in hits:
                from scripts.entities.player import Player
                if isinstance(hit.entity, Player):
                    hit.entity.damage(self.attack_damage, DamageSource(self.pos))
                    self.attack_cooldown_timer = self.attack_cooldown
        else:
            self.attack_cooldown_timer -= self.app.deltatime

        print("enemy: ", self, " ", self.velocity)
        super().update()

    def damage(self, damage, source: DamageSource):
        super().damage(damage, source)

    def render(self, offset = [0, 0]):
        offset = np.array(offset)
        sprite = super().render(offset)
        color_to_add = np.array([0, 64, 64]) * self.attack_cooldown_timer / self.attack_cooldown
        color_to_sub = np.array([64, 0, 0]) * self.attack_cooldown_timer / self.attack_cooldown
        sprite.fill(color_to_add, special_flags=pygame.BLEND_RGB_ADD)
        sprite.fill(color_to_sub, special_flags=pygame.BLEND_RGB_SUB)
        self.app.display.blit(sprite, self.pos - self.size * 0.5 - offset)
