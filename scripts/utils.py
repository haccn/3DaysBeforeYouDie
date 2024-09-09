import pygame

from scripts.const import *

def load_img(path):
    return pygame.image.load(f"{PATH}{path}")
