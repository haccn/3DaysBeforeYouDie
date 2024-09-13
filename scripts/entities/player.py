import pygame

import numpy as np

from scripts.entities.entity import Entity, DamageSource
from scripts.entities.enemy import Enemy
from scripts.utils import *

class Player(Entity):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.sprite = load_img("player/player.png")

        self.speed = 100.
        self.attack_distance = 20.
        self.attack_damage = 1

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
                        hits = raycast(Ray(self.pos, self.pos + self.forward * self.attack_distance), self.app.enemies)
                        for hit in hits:
                            if isinstance(hit.entity, Enemy):
                                hit.entity.damage(self.attack_damage, DamageSource(self.pos))
                elif self.mode == "Building":
                    print("Yes")
                    self.app.building_system.place_building()

                #print(self.mode)


    def update(self):
        self.input()
        input_vec = normalize(np.array([
            float(self.app.keys_pressed[pygame.K_d] | self.app.keys_pressed[pygame.K_RIGHT]) -
                float(self.app.keys_pressed[pygame.K_a] | self.app.keys_pressed[pygame.K_LEFT]),
            float(self.app.keys_pressed[pygame.K_s] | self.app.keys_pressed[pygame.K_DOWN]) -
                float(self.app.keys_pressed[pygame.K_w] | self.app.keys_pressed[pygame.K_UP]),
        ]))
        self.velocity = input_vec * self.speed
        super().update()

    def render(self, offset=np.array([0, 0])):
        if self.mode == "Building":
            self.app.building_system.preview()
        sprite = pygame.transform.scale(self.sprite, self.size)
        self.app.display.blit(sprite, self.pos - offset)

        # FOR DEBUGGING RAYCASTING
        hits = raycast(Ray(self.pos, self.pos + self.forward * self.attack_distance), self.app.enemies)
        color = (0, 255, 0) if len(hits) > 0 else (128, 128, 128)
        pygame.draw.line(self.app.display, color, self.pos - offset, self.pos + self.forward * self.attack_distance - offset)
        for hit in hits:
            pygame.draw.circle(self.app.display, (0, 255, 0), hit.point - offset, 5)

        super().render(offset)
