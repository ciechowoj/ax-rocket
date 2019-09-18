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

class Spacecraft:
    ENGINES = [(vec2(13.5, 5.5), vec2(-0.759256, -0.650791)), (vec2(7.5, 12.5), vec2(-0.759256, -0.650791)), (vec2(7.5, 48.5), vec2(-0.759256, +0.650791)), (vec2(13.5, 55.5), vec2(-0.759256, +0.650791))]
    CENTER = vec2(44.5, 30.5)
    MASS = 1500
    SPRITE = pygame.image.load("data/spacecraft.png")
    EPSILON = 0.1
    RADIUS = 60.0

    class Particle:
        def __init__(self, position, velocity):
            self.position = position
            self.velocity = velocity
            self.time = 0.2

    def __init__(self, position):
        self.position = position
        self.direction = 0.0
        self.linear_velocity = vec2(0.0, 0.0)
        self.angular_velocity = 0.0
        self.engine_force = 0.0
        self.external_force = vec2()
        self.particles = []
        self.mass = Spacecraft.MASS
        self.radius = Spacecraft.RADIUS
        self.mask = pygame.mask.from_surface(Spacecraft.SPRITE)

    def on_update(self, delta, current):
        direction_vector = rotate2(vec2(1, 0), self.direction)
        force = direction_vector * self.engine_force + self.external_force
        linear_acceleration = force / Spacecraft.MASS

        if self.engine_force > 0.0:
            engines = [(rotate2(x[0] - Spacecraft.CENTER, self.direction) + self.position, rotate2(x[1], self.direction)) for x in Spacecraft.ENGINES]
            for i in range(int(500 * delta)):
                for e in engines:
                    self.particles.append(Spacecraft.Particle(e[0], self.linear_velocity + rotate2(e[1] * 100, random() - 0.5)))

        for p in self.particles:
            p.position += p.velocity * delta

        self.linear_velocity += linear_acceleration * delta
        self.position += self.linear_velocity * delta
        self.direction += (self.angular_velocity * delta) % (2 * pi)

    def on_redraw(self, surface, delta, viewport):
        rotated = pygame.transform.rotate(Spacecraft.SPRITE, self.direction / pi * 180)

        offset = vec2(Spacecraft.SPRITE.get_size()) * 0.5 - Spacecraft.CENTER
        offset = rotate2(offset, self.direction)
        position = -vec2(rotated.get_size()) * 0.5 + offset + self.position - viewport
        
        i, s = 0, len(self.particles)
        while i < s:
            p = self.particles[i]
            pygame.gfxdraw.filled_circle(surface, int(p.position.x - viewport.x), int(p.position.y - viewport.y), 2, (255, int(255 * p.time * 5), 0, int(255 * p.time * 5)) )
            p.time -= delta
            if p.time < 0.0:
                del self.particles[i]
                i -= 1
                s -= 1
            i += 1

        surface.blit(rotated, position.intcpl())
        self.sprite = rotated
        self.mask = pygame.mask.from_surface(rotated)