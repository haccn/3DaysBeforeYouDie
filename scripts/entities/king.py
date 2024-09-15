from scripts.entities.entity import Entity, DamageSource
import scripts.utils as utils
import pygame
import numpy as np
import random

class King(Entity):
    def __init__(self, *args, health=5, **kwargs):
        super().__init__(*args, health=health, **kwargs)
        self.pos = np.array([-50, -50])
        self.target_pos = np.array([0, 0])
        self.wander_distance = 100

        self.speed = 100
        self.acceleration_speed = 500

        self.move_cooldown = 1.
        self.move_cooldown_timer = 0

        self.sprite.fill((0, 0, 255))

    def update(self):
        dir_to_target = self.target_pos - self.pos
        if np.linalg.norm(self.velocity) < self.speed and np.linalg.norm(dir_to_target) > 5:
            self.acceleration = dir_to_target * self.acceleration_speed
        else:
            self.acceleration = np.zeros(2)
        self.forward = utils.normalize(self.velocity)

        if self.move_cooldown_timer <= 0:
            self.target_pos = np.array([
                self.pos[0] + random.randrange(0, self.wander_distance),
                self.pos[1] + random.randrange(0, self.wander_distance)
            ])
            self.move_cooldown_timer = self.move_cooldown
        else:
            self.move_cooldown_timer -= self.app.deltatime

        super().update()

    def damage(self, damage, source: DamageSource):
        super().damage(damage, source)
        if self.health <= 0:
            del self.app.king
            utils.del_from_list(self.app.entities, self)

    def render(self, offset = [0, 0]):
        offset = np.array(offset)
        sprite = super().render(offset)
        self.app.display.blit(sprite, self.pos - self.size * 0.5 - offset)
