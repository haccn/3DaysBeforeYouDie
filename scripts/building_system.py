import pygame

from scripts.const import *
from scripts.utils import *

class Building_System():
    def __init__(self,app):
        self.app = app

        self.buildings = []
        self.place_pos = [0,0]
        self.building_types = {"stonewall" : {"b_type" : "wall", "health" : 5}}
        
        self.placement = 0 

    def get_wall(self,pos):
        for build in self.buildings:
            if build["pos"] == list(pos):
                return build
        return False

    def match_wall(self,wall,pos):
        other_wall = self.get_wall(pos)
        if other_wall:
            if wall["b_type"] == other_wall["b_type"]:
                return True
        
        return False
            

    def place_wall(self,wall_type,size,health):
        img = load_img(f"tiles/buildings/{wall_type}/center.png")

        wall = {"b_type" : wall_type,"pos" : self.place_pos,"size" : size,"img" : img,"rect" : pygame.Rect(self.place_pos,size)}
        walls = [self.match_wall(wall,(wall["pos"][0],wall["pos"][1]-TILE_SIZE[1])),
                 self.match_wall(wall,(wall["pos"][0],wall["pos"][1]+TILE_SIZE[1])),
                 self.match_wall(wall,(wall["pos"][0]+TILE_SIZE[0],wall["pos"][1])),
                 self.match_wall(wall,(wall["pos"][0]-TILE_SIZE[0],wall["pos"][1]))]
    
        if walls[0] and walls[1]:
            img = load_img(f"tiles/buildings/{wall_type}/side.png")

        if walls[2] and walls[3]:
            img = pygame.transform.rotate(load_img(f"tiles/buildings/{wall_type}/side.png"),90)

        if walls[0] and walls[3]:
            img = load_img(f"tiles/buildings/{wall_type}/corner.png")

        if walls[0] and walls[2]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall_type}/corner.png"),False,True)

        if walls[1] and walls[3]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall_type}/corner.png"),True,False)

        if walls[1] and walls[2]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall_type}/corner.png"),True,True)

        wall = {"b_type" : wall_type,"pos" : self.place_pos,"size" : size,"img" : img,"rect" : pygame.Rect(self.place_pos,size),"health" : health}

        self.buildings.append(wall)
        return wall

    def update_wall(self,wall):

        img = load_img(f"tiles/buildings/{wall["b_type"]}/center.png")

        corner = load_img(f"tiles/buildings/{wall["b_type"]}/corner.png")

        wall = {"b_type" : wall["b_type"],"pos" : wall["pos"],"size" : wall["size"],"img" : img,"rect" : pygame.Rect(wall["pos"],wall["size"])}
        walls = [self.match_wall(wall,(wall["pos"][0],wall["pos"][1]-TILE_SIZE[1])),
                self.match_wall(wall,(wall["pos"][0],wall["pos"][1]+TILE_SIZE[1])),
                self.match_wall(wall,(wall["pos"][0]+TILE_SIZE[0],wall["pos"][1])),
                self.match_wall(wall,(wall["pos"][0]-TILE_SIZE[0],wall["pos"][1]))]
    
        if walls[0] and walls[1]:
            img = load_img(f"tiles/buildings/{wall["b_type"]}/side.png")

        if walls[2] and walls[3]:
            img = pygame.transform.rotate(load_img(f"tiles/buildings/{wall["b_type"]}/side.png"),90)

        if walls[0] and walls[3]:
            img = load_img(f"tiles/buildings/{wall["b_type"]}/corner.png")

        if walls[0] and walls[2]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall["b_type"]}/corner.png"),True,False)

        if walls[1] and walls[3]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall["b_type"]}/corner.png"),False,True)

        if walls[1] and walls[2]:
            img = pygame.transform.flip(load_img(f"tiles/buildings/{wall["b_type"]}/corner.png"),True,True)
    
        wall["img"] = img

    def place(self):
        placement = self.building_types[list(self.building_types.keys())[self.placement]]

        if placement["b_type"] == "wall":
            wall = self.place_wall(list(self.building_types.keys())[self.placement],(16,16),placement["health"])
            walls = [self.get_wall((wall["pos"][0],wall["pos"][1]-TILE_SIZE[1])),
                self.get_wall((wall["pos"][0],wall["pos"][1]+TILE_SIZE[1])),
                self.get_wall((wall["pos"][0]+TILE_SIZE[0],wall["pos"][1])),
                self.get_wall((wall["pos"][0]-TILE_SIZE[0],wall["pos"][1]))]
            for building in self.buildings:
                for wall in walls:
                    if not wall:
                        continue
                    if wall == building:
                        print("yes")
                        self.update_wall(building)

        if placement["b_type"] == "tower":
            self.place_building("tower",list(self.building_types.keys())[self.placement],5)

    def place_building(self,b_type,name,health):

        img = load_img(f"tiles/buildings/{b_type}/{name}")

        self.buildings.append({"b_type" : b_type,"pos" : self.place_pos,"size" : img.get_size(),
                               "img" : img,"rect" : pygame.Rect(self.place_pos,img.get_size()),"health" : health})


    def update(self):
        self.place_pos = list(pygame.Vector2(self.app.mouse.pos[0]-self.app.player.pos[0]+1,self.app.mouse.pos[1]-self.app.player.pos[1]+1).normalize())

        self.place_pos[0] = round(self.place_pos[0]) * TILE_SIZE[0] + (int(self.app.player.rect.centerx / TILE_SIZE[0]) * TILE_SIZE[0])
        self.place_pos[1] = round(self.place_pos[1]) * TILE_SIZE[1] + (int(self.app.player.rect.centery / TILE_SIZE[1]) * TILE_SIZE[1])

        #print(self.place_pos)

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
