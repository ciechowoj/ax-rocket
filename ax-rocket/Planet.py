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

class Planet:
    SPRITES = [pygame.image.load("data/planet" + str(x) + ".png") for x in range(10)]
    CENTER = vec2(32.5, 30.5)
    MASS = 3254
    RADIUS = 1000.0

    def __init__(self, position):
        self.position = position
        self.direction = 0.0
        self.planet = randint(0, len(Planet.SPRITES) - 1)

        self.angular_velocity = random() * 0.1 + 0.1
        self.radius = Planet.RADIUS
        self.mask = pygame.mask.from_surface(Planet.SPRITES[self.planet])
        self.mass = self.mask.count()

    def on_redraw(self, surface, delta, viewport):
        position = self.position - viewport
        if circleRectangleIntersect(position, self.radius, vec2(surface.get_size()), vec2(surface.get_size())):
            self.direction += (self.angular_velocity * delta) % (2 * pi)
            rotated = Planet.SPRITES[self.planet]
            position -= vec2(rotated.get_size()) * 0.5
            surface.blit(rotated, position.intcpl())
            self.sprite = rotated
