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

class Asteroid:
    SPRITES = [pygame.image.load("data/asteroid" + str(x) + ".png") for x in range(5)]
    CENTER = vec2(32.5, 30.5)
    MASS = 3254
    RADIUS = 80.0

    def __init__(self, position, velocity):
        self.position = position
        self.direction = 0.0
        self.index = randint(0, len(Asteroid.SPRITES) - 1)
        self.linear_velocity = velocity
        self.angular_velocity = random() + 0.5
        self.radius = Asteroid.RADIUS
        self.mask = pygame.mask.from_surface(Asteroid.SPRITES[self.index])
        self.mass = self.mask.count() * 0.3

    def on_update(self, delta):
        self.position += self.linear_velocity * delta 

    def on_redraw(self, surface, delta, viewport):
        position = self.position - viewport
        if circleRectangleIntersect(self.position - viewport, self.radius, vec2(surface.get_size()), vec2(surface.get_size())):
            self.direction += (self.angular_velocity * delta) % (2 * pi)
            rotated = pygame.transform.rotate(Asteroid.SPRITES[self.index], self.direction / pi * 180)
            position -= vec2(rotated.get_size()) * 0.5
            surface.blit(rotated, position.intcpl())
            self.sprite = rotated
            self.mask = pygame.mask.from_surface(rotated)