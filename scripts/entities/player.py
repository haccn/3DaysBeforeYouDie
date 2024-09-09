import pygame

from scripts.entities.entity import Entity

class Player(Entity):
    def __init__(self,app,pos,size,health):
        super().__init__(app, pos, size,health)

    def input(self):
        for event in self.app.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.movement[2] = True
                if event.key == pygame.K_s:
                    self.movement[3] = True
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movement[2] = False
                if event.key == pygame.K_s:
                    self.movement[3] = False
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False

    
    def update(self):
        self.input()
        return super().update()
