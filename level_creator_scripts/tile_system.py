import pygame

import json

import os

from scripts.utils import *

from scripts.const import *

class tile_System():
    def __init__(self,app,tiles=[]):
        
        self.app = app

        self.tiles = tiles

        self.tile_types = ["Grass","Rock","Water"]

        self.tile_type = 0

        self.tile_index = 0

        self.snap = False
        
        self.cd = self.app.deltatime



    def pick_tile(self,):
        keys = pygame.key.get_pressed()
        
        for event in self.app.all_events:
            if event.type == pygame.MOUSEWHEEL:
                if self.debounce(.2):
                    if keys[pygame.K_LSHIFT]:
                        self.tile_type += event.y
                    else:
                        self.tile_index += event.y
                    if self.tile_type < 0:
                        self.tile_type = 0
                    if self.tile_type > len(self.tile_types) - 1:
                        self.tile_type = len(self.tile_types) - 1
                    if self.tile_index < 0:
                        self.tile_index = 0
                    if self.tile_index > len(os.listdir(f"assets/tiles/{self.tile_types[self.tile_type]}")) - 1:
                        self.tile_index = len(os.listdir(f"assets/tiles/{self.tile_types[self.tile_type]}")) - 1


    def add_tile(self,pos,tile_type,size=(16,16)):
        if self.snap:
            pos = (int(int(pos[0] / size[0]) * size[0]),int(int(pos[1] / size[1]) * size[1]))
        for tile in self.tiles:
            if tile["pos"] == pos:
                return
            
        path = f'tiles/{tile_type}'
        self.tiles.append({"pos" : pos,"size" : size,"tile_type" : tile_type,
                           "rect" : pygame.Rect(pos[0],pos[1],size[0],size[1]),"img" : os.listdir(f"assets/{path}")[self.tile_index]})

    def tile_preview(self,pos,size=TILE_SIZE):
        if self.snap:
            pos = (int(pos[0] / size[0]) * size[0],int(pos[1] / size[1]) * size[1])

        img = load_img(f"tiles/{self.tile_types[self.tile_type]}/{os.listdir(f"assets/tiles/{self.tile_types[self.tile_type]}")[self.tile_index]}")
        img.set_alpha(100)
        self.app.display.blit(img,pos)


    def remove_tile(self,mouse_pos):
        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos[0],mouse_pos[1]):
                self.tiles.remove(tile)

    def loadsave(self,name):
        f = open("tile_saves/" + name,"r")
        self.tiles = json.load(f)

        for tile in self.tiles:
            tile["rect"] = pygame.Rect(tile["pos"][0],tile["pos"][1],tile["size"][0],tile["size"][1])

        f.close()

    def save(self,name):
        f = open("tile_saves/" + name,"w")
        savefile = json.dumps([{"pos" : (int(tile["pos"][0]),int(tile["pos"][1])), "size" : tile["size"], "tile_type" : tile["tile_type"], "img" : tile["img"]} for tile in self.tiles])
        f.write(savefile)

        f.close()

    def get_tile(self,pos):
        for tile in self.tiles:
            if tuple(tile["pos"]) == tuple(pos):
                return tile
    def match_tile(self,tile_0,tile_1):
        if tile_0 is None or tile_1 is None:
            return False
        else:
            return tile_0["tile_type"] == tile_1["tile_type"]   
        
    def auto_tile(self):
        for tile in self.tiles:


            top_tile = self.get_tile((tile["pos"][0],tile["pos"][1] - TILE_SIZE[1]))

            right_tile = self.get_tile((tile["pos"][0] + TILE_SIZE[0],tile["pos"][1]))

            bottom_tile = self.get_tile((tile["pos"][0],tile["pos"][1] + TILE_SIZE[1]))

            left_tile = self.get_tile((tile["pos"][0] - TILE_SIZE[0],tile["pos"][1]))
            
            print(tile["pos"])

            tile["img"] = "single.png"

            if self.match_tile(tile,bottom_tile):
                tile["img"] = "singleT.png"
            if self.match_tile(tile,left_tile):
                tile["img"] = "singleR.png"
            if self.match_tile(tile,right_tile):
                tile["img"] = "singleL.png"
            if self.match_tile(tile,top_tile):
                tile["img"] = "singleB.png"

            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,right_tile):
                tile["img"] = "topL.png"
            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "topR.png"
            if self.match_tile(tile,top_tile) and self.match_tile(tile,right_tile):
                tile["img"] = "bottomL.png"
            if self.match_tile(tile,top_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "bottomR.png"

            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,right_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "top.png"
            if self.match_tile(tile,top_tile) and self.match_tile(tile,right_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "bottom.png"
            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,top_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "right.png"
            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,top_tile) and self.match_tile(tile,right_tile):
                tile["img"] = "left.png"
            
            if self.match_tile(tile,bottom_tile) and self.match_tile(tile,top_tile) and self.match_tile(tile,right_tile) and self.match_tile(tile,left_tile):
                tile["img"] = "Middle.png"


    # def group_tiles(self):
    #     rects = []

    #     tiles = []

    #     for tile in self.tiles:
    #         tile_up = self.get_tile((tile["pos"][0] + TILE_SIZE[0],tile["pos"][1] - TILE_SIZE[1]))
    #         while tile_up is not None:
    #             tile_up = self.get_tile((tile_up["pos"][0] + TILE_SIZE[0],tile_up["pos"][1] - TILE_SIZE[1]))
    #             if tile_up is not None:
    #                 tiles.append(tile_up)

    #     return rects
        


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_t]:
            self.auto_tile()
        if keys[pygame.K_s] and keys[pygame.K_LCTRL]:
            self.save("Tileset_0")
        if keys[pygame.K_o] and keys[pygame.K_LCTRL]:
            self.loadsave("Tileset_0")
        if keys[pygame.K_g]:
            if self.debounce(.2):
                self.snap = not self.snap

        self.pick_tile()

    def debounce(self,dur):
        waited = False

        if self.app.deltatime - self.cd > dur:
            waited = True
            self.cd = self.app.deltatime

        return waited

    def render(self,offset=(0,0)):
        for tile in self.tiles:
            self.app.display.blit(pygame.transform.scale(load_img(f"tiles/{tile["tile_type"]}/{tile["img"]}"),tile["size"]),
                                  (tile["pos"][0] - offset[0],tile["pos"][1] - offset[1]))


