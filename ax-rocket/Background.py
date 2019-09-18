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

class Background:
    class QuadTree:
        def __init__(self, position, size, depth):
            self.depth = depth
            self.size = size
            self.position = position
            if depth != 0:
                child_size = size * 0.6
                child_depth = depth - 1
                p0 = vec2(position.x + child_size.x, position.y + child_size.y)
                p1 = vec2(position.x - child_size.x, position.y + child_size.y)
                p2 = vec2(position.x + child_size.x, position.y - child_size.y)
                p3 = vec2(position.x - child_size.x, position.y - child_size.y)
                self.children = (Background.QuadTree(p0, child_size, child_depth), Background.QuadTree(p1, child_size, child_depth), Background.QuadTree(p2, child_size, child_depth), Background.QuadTree(p3, child_size, child_depth))
            else:
                self.children = []
            self.elements = []

        def insert(self, element):
            for x in self.children:
                if circleRectangleIntersect(element.position, element.radius, x.position, x.size):
                    x.insert(element)
                    return
            self.elements.append(element)
                
        def redraw(self, surface, viewport):
            for x in self.elements:
                x.redraw(surface, viewport)
            for x in self.children:
                if rectRectIntersect(x.position - viewport, x.size, vec2(surface.get_size()) * 0.5, vec2(surface.get_size()) * 0.5):
                    x.redraw(surface, viewport)


    class Star:
        COLORS = [(255, 190, 190), (190, 255, 190), (255, 255, 255), (150, 150, 255)]
        def __init__(self, position, radius):
            self.position = position
            self.radius = radius

        def redraw(self, surface, viewport):
            position = self.position.intcpl()
            color = Background.Star.COLORS[(position[0] + position[1]) % len(Background.Star.COLORS)]
            position = (self.position - viewport).intcpl()
            pygame.gfxdraw.filled_circle(surface, position[0], position[1], self.radius, color + (50,))
            pygame.gfxdraw.filled_circle(surface, position[0], position[1], self.radius - 1, color + (128,))
            if self.radius - 3 > 0:
                pygame.gfxdraw.filled_circle(surface, position[0], position[1], self.radius - 3, color + (255,))

    def __init__(self, size):
        self.quad_tree = Background.QuadTree(vec2(), size, 3)
        for i in range(2000):
            self.quad_tree.insert(Background.Star(vec2(random() * 2.0 - 1.0, random() * 2.0 - 1.0) * size, randint(2, 5)))

    def on_redraw(self, surface, delta, viewport):
        self.quad_tree.redraw(surface, viewport)
