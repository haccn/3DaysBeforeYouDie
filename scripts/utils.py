import pygame

import numpy as np

from scripts.const import *

def normalize(vec):
    return vec / np.linalg.norm(vec + np.finfo(vec.dtype).eps)

def load_img(path):
    return pygame.image.load(f"{PATH}{path}")
