import pygame

from scripts.utils import *

class Mouse():
    def __init__(self,app,pos,size):
        self.app = app
        self.pos = list(pos)
        self.size = size
        self.mouse_rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
    
    def update(self):
        self.pos = list(pygame.mouse.get_pos())

        self.pos[0] = self.pos[0] * (self.app.display.get_size()[0] / self.app.screen_size[0]) + self.app.offset[0]
        self.pos[1] = self.pos[1] * (self.app.display.get_size()[1] / self.app.screen_size[1]) + self.app.offset[1]

        self.mouse_rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def click(self):
        return pygame.mouse.get_pressed()[0]

    def right_click(self):
        return pygame.mouse.get_pressed()[2]

    def render(self):
        self.app.display.blit(pygame.transform.scale(load_img("mouse/mouse.png"),self.size),self.pos)