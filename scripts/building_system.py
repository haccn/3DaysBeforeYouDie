import pygame

from scripts.const import *
from scripts.utils import *

class Building_System():
    def __init__(self,app):
        self.app = app

        self.buildings = []
        self.place_pos = [0,0]
        self.building_types = {"Wall" : {"pos" : self.place_pos,"size" : (16,16),"img" : load_img("tiles/buildings/stoneWall/bottom.png"),"rect" : pygame.Rect(self.place_pos,(16,16))},
                               "Tower" : {"pos" : self.place_pos,"size" : (12,28),"img" : load_img("tiles/buildings/tower/woodenTower.png"),"rect" : pygame.Rect(self.place_pos,(32,32))}
                               }

        self.placement = 0

    #def place_wall(self):


    def place_building(self):
        building = list(self.building_types.keys())[self.placement]

        building = {"pos" : self.place_pos,"size" : self.building_types[building]["size"],"img" : self.building_types[building]["img"],"rect" : pygame.Rect(self.place_pos,self.building_types[building]["size"])}

        for build in self.buildings:
            if build["rect"].colliderect(building["rect"]):
                return

        self.buildings.append(building)

        print(building)

        #print(self.buildings)


    def update(self):
        self.place_pos = list(pygame.Vector2(self.app.mouse.pos[0]-self.app.player.pos[0]+1,self.app.mouse.pos[1]-self.app.player.pos[1]+1).normalize())

        self.place_pos[0] = round(self.place_pos[0]) * TILE_SIZE[0] + (int(self.app.player.rect.centerx / TILE_SIZE[0]) * TILE_SIZE[0])
        self.place_pos[1] = round(self.place_pos[1]) * TILE_SIZE[1] + (int(self.app.player.rect.centery / TILE_SIZE[1]) * TILE_SIZE[1])

        print(self.place_pos)

    def select(self):
        for event in self.app.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.placement = min(len(self.building_types),self.placement + 1)
                if event.key == pygame.K_q:
                    self.placement = max(0,self.placement - 1)

    def render(self,offset=(0,0)):
        #print(self.buildings)
        for building in self.buildings:
            #print(building)
            self.app.display.blit(building["img"],(building["pos"][0]-offset[0],building["pos"][1]-offset[1]))

    def preview(self):
        pygame.draw.rect(self.app.display,(0,255,0,125),pygame.Rect((self.place_pos[0]-self.app.offset[0],self.place_pos[1]-self.app.offset[1]),(16,16)))
