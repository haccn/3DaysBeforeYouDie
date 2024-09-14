import sys

import pygame

import numpy as np

from scripts.const import *

def normalize(vec):
    return vec / np.linalg.norm(vec + np.finfo(vec.dtype).eps)

def load_img(path):
    return pygame.image.load(f"{PATH}{path}")

def del_from_list(l: list, obj: object):
    for i, o in enumerate(l):
        if o == obj:
            del l[i]
            break

class Ray:
    def __init__(self, p1, p2, is_infinite: bool = False):
        self.p1 = p1
        self.p2 = p2
        self.is_infinite = is_infinite

class RayResult:
    def __init__(self, point, entity):
        self.point = point
        self.entity = entity

def raycast(ray: Ray, entities) -> [RayResult]:
    ray_length = sys.float_info.max if ray.is_infinite else np.linalg.norm(ray.p2 - ray.p1)
    hits = []
    for entity in entities:
        intersections = entity.rect.clipline(ray.p1, ray.p2)
        for isect in intersections:
            if np.linalg.norm(isect - ray.p1) < ray_length:
                hits.append(RayResult(np.array(isect), entity))
    return hits
