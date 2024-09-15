from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np

class Enemy(Entity):
    def __init__(self, *args, pos=[100., 100.], health=3, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array(pos)

        self.speed = 30
        self.acceleration_speed = 700

        self.attack_distance = 12

        self.attack_damage = 1
        self.attack_cooldown = 3.
        self.attack_cooldown_timer = 0

        self.sprite.fill((255, 0, 0))

    def update(self):
        dir_to_king = utils.normalize(self.app.king.pos - self.pos)
        if np.linalg.norm(self.velocity) < self.speed:
            self.acceleration = dir_to_king * self.acceleration_speed
        else:
            self.acceleration = np.zeros(2)

        self.forward = utils.normalize(self.app.player.pos - self.pos)

        if self.attack_cooldown_timer <= 0:
            hit_entities = [hit.entity for hit in utils.raycast(utils.Ray(self.pos, self.pos + self.forward * self.attack_distance), [self.app.player])]
            for entity in list(set(hit_entities)):
                entity.damage(self.attack_damage, DamageSource(self.pos))
                self.attack_cooldown_timer = self.attack_cooldown
        else:
            self.attack_cooldown_timer -= self.app.deltatime

        super().update()

    def damage(self, damage, source: DamageSource):
        print("damaged: ", damage, "hp: ",self.health)
        super().damage(damage, source)
        print("hp: ",self.health)
        if self.health <= 0:
            utils.del_from_list(self.app.enemies, self)
            utils.del_from_list(self.app.entities, self)

    def render(self, offset = [0, 0]):
        offset = np.array(offset)
        sprite = super().render(offset)
        color_to_add = np.array([0, 64, 64]) * self.attack_cooldown_timer / self.attack_cooldown
        color_to_sub = np.array([64, 0, 0]) * self.attack_cooldown_timer / self.attack_cooldown
        sprite.fill(color_to_add, special_flags=pygame.BLEND_RGB_ADD)
        sprite.fill(color_to_sub, special_flags=pygame.BLEND_RGB_SUB)
        self.app.display.blit(sprite, self.pos - self.size * 0.5 - offset)
