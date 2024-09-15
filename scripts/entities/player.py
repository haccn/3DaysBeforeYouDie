import pygame

import numpy as np

from scripts.entities.entity import Entity, DamageSource
from scripts.utils import *

class Player(Entity):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,health=5,size=np.array([9, 16]),kinetic_friction=5.,**kwargs)

        self.sprite = load_img("player/player.png")

        self.speed = 70.
        self.acceleration_speed = 1000.

        self.resources = {"money" : 0}
        self.modes = ["Fighting","Building"]
        self.mode = "Fighting"

    def input(self):
        for event in self.app.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    next_mode = self.modes.index(self.mode) + 1
                    if next_mode >= len(self.modes):
                        next_mode = 0
                    self.mode = self.modes[next_mode]
                if self.mode == "Building":
                    if event.key == pygame.K_q:
                        self.app.building_system.placement = max(0,self.app.building_system.placement - 1)
                    if event.key == pygame.K_e:
                        self.app.building_system.placement = min(len(self.app.building_system.building_types) - 1,self.app.building_system.placement + 1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == "Fighting":
                    if event.button == 1:
                        hit_entities = [hit.entity for hit in raycast(Ray(self.pos, self.pos + self.forward * self.attack_distance), self.app.enemies)]
                        for entity in list(set(hit_entities)):
                            from scripts.entities.enemy import Enemy
                            if isinstance(entity, Enemy):
                                entity.damage(self.attack_damage, DamageSource(self.pos))
                elif self.mode == "Building":
                    self.app.building_system.place()
                    self.app.building_system.delete_building()

                #print(self.mode)

    def damage(self, damage, source: DamageSource):
        super().damage(damage, source)
        if self.health <= 0:
            del self.app.player
            del_from_list(self.app.entities, self)

    def update(self):
        self.input()

        input_vec = normalize(np.array([
            float(self.app.keys_pressed[pygame.K_d] | self.app.keys_pressed[pygame.K_RIGHT]) -
                float(self.app.keys_pressed[pygame.K_a] | self.app.keys_pressed[pygame.K_LEFT]),
            float(self.app.keys_pressed[pygame.K_s] | self.app.keys_pressed[pygame.K_DOWN]) -
                float(self.app.keys_pressed[pygame.K_w] | self.app.keys_pressed[pygame.K_UP]),
        ]))
        if np.linalg.norm(self.velocity) < self.speed:
            self.acceleration = input_vec * self.acceleration_speed
        else:
            self.acceleration = np.zeros(2)

        self.forward = normalize(self.app.mouse.pos - self.pos)

        super().update()

    def render(self, offset=[0, 0]):
        offset = np.array(offset)
        sprite = super().render(offset)
        sprite = pygame.transform.scale(sprite, self.size)
        self.app.display.blit(sprite, self.pos - offset)
        if self.mode == "Building":
            self.app.building_system.preview()
        rect = self.rect
        rect.x = self.pos[0] - offset[0]
        rect.y = self.pos[1] - offset[1]
        #pygame.draw.rect(self.app.display,(0,0,0),rect)
