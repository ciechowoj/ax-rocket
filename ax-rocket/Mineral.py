# brief         part of ax-spacecraft game
# author        Wojciech Szęszoł keepitsimplesirius[at]gmail.com
# encoding      UTF-8 with BOM
# end of line   LF
# tab           4x space

import pygame
import pygame.gfxdraw
from pygame.locals import *
from axmath import *
from random import random
from random import randint

class Mineral:
    SPRITES = [pygame.image.load("data/" + x) for x in ["fuel.png", "copper.png", "silver.png", "gold.png", "platinum.png"]]
    CENTER = vec2(32.5, 30.5)
    MASS = 3254
    RADIUS = 50.0

    def __init__(self, position):
        self.position = position
        self.direction = 0.0
        self.index = randint(0, len(Mineral.SPRITES) - 1)
        self.angular_velocity = (random() - 0.5) * 2.0
        self.radius = Mineral.RADIUS
        self.mask = pygame.mask.from_surface(Mineral.SPRITES[self.index])

    def on_redraw(self, surface, delta, viewport):
        position = self.position - viewport
        if circleRectangleIntersect(self.position - viewport, self.radius, vec2(surface.get_size()), vec2(surface.get_size())):
            self.direction += (self.angular_velocity * delta) % (2 * pi)
            rotated = pygame.transform.rotate(Mineral.SPRITES[self.index], self.direction / pi * 180)
            position -= vec2(rotated.get_size()) * 0.5
            surface.blit(rotated, position.intcpl())
            self.sprite = rotated
            self.mask = pygame.mask.from_surface(rotated)