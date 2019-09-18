# brief         part of ax-rocket game
# author        Wojciech Szęszoł keepitsimplesirius[at]gmail.com
# encoding      UTF-8 with BOM
# end of line   LF
# tab           4x space

import pygame
import pygame.gfxdraw
from pygame.locals import *
from random import random
from random import randint

# init pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init(buffer = 64)
if pygame.font.get_init() == False:
    input("Cannot initialize pygame.font module...")
if pygame.mixer.get_init() == False:
    input("Cannot initialize pygame.mixer module...")
pygame.mouse.set_visible(False)

# init game modules
from Spacecraft import *
from Planet import *
from Background import *
from Asteroid import *
from Mineral import *

# auxiliary functions
def random2():
    return random() * 2.0 - 1.0

# create game
ASTEROID_RADIUS = 5000
ASTEROID_THRESHOLD = 0.0001
ASTEROID_VELOCITY = 500
GAMEPLAY_RADIUS = 3000
CELESTIAL_RADIUS = 2000
START_AREA_RADIUS = 150
DAMAGE_FACTOR = 0.00005
FUEL_USAGE = 0.0000001

def drawPlanets(number):
    planets = []
    i = 0
    while i < number:
        position = vec2(random2() * CELESTIAL_RADIUS, random2() * CELESTIAL_RADIUS)
        if circleCircleCollide(position, Planet.RADIUS, vec2(), CELESTIAL_RADIUS) and not circleCircleCollide(position, Planet.RADIUS, vec2(), START_AREA_RADIUS):
            j, s = 0, len(planets)
            while j < s:
                if circleCircleCollide(position, Planet.RADIUS, planets[j].position, Planet.RADIUS):
                    break
                j += 1
            if j == s:
                planets.append(Planet(position))
                i += 1
    return planets

def drawMinerals(number, planets):
    minerals = []
    i = 0
    while i < number:
        position = vec2(random2() * GAMEPLAY_RADIUS, random2() * GAMEPLAY_RADIUS)
        if circleCircleCollide(position, Mineral.RADIUS, vec2(), GAMEPLAY_RADIUS) and not circleCircleCollide(position, Mineral.RADIUS, vec2(), START_AREA_RADIUS):
            j, s = 0, len(planets)
            while j < s:
                if circleCircleCollide(position, Mineral.RADIUS, planets[j].position, Planet.RADIUS):
                    break
                j += 1
            if j == s:
                minerals.append(Mineral(position))
                i += 1
    return minerals

def drawAsteroid(planets):
    position = rotate2(vec2(ASTEROID_RADIUS, 0), random() * 2 * pi)
    velocity = rotate2((-position).normal(), random() * 2.0 - 1.0) * ASTEROID_VELOCITY * (random() + 1)
    return Asteroid(position, velocity)

def getGravity(spacecraft, planets):
    GRAVITY = 70.0
    gravity = vec2()
    for p in planets:
        vector = (p.position - spacecraft.position)
        distance = vector.length()
        vector = vector.normal()
        gravity += vector * (GRAVITY * p.mass * spacecraft.mass / (distance * distance))
    return gravity

def collide(st_object, nd_object):
    if circleCircleCollide(st_object.position, st_object.radius, nd_object.position, nd_object.radius):
        offset = (nd_object.position - vec2(nd_object.mask.get_size()) * 0.5) - (st_object.position - vec2(st_object.mask.get_size()) * 0.5)
        return st_object.mask.overlap(nd_object.mask, offset.intcpl())
    else:
        return False

def drawVector(surface, point, vector, color = (0, 255, 255)):
    pygame.draw.line(surface, color, point.intcpl(), (point + vector).intcpl(), 1)
    pygame.draw.circle(surface, (255, 0, 0), point.intcpl(), 32, 1)

spacecraft = Spacecraft(vec2())
background = Background(vec2(GAMEPLAY_RADIUS * 2.1, GAMEPLAY_RADIUS * 2.1))
planets = drawPlanets(4)
minerals = drawMinerals(50, planets)
asteroids = []

health = 1.0
fuel = 1.0
score = 0

font = pygame.font.Font("data/pirulen.ttf", 32)
bigfont = pygame.font.Font("data/pirulen.ttf", 64)

TIME_STEP = 0.01
oldTime = pygame.time.get_ticks() * 0.001
newTime = pygame.time.get_ticks() * 0.001
deltaTime = 0
screen = pygame.display.set_mode( (1024, 768), pygame.FULLSCREEN )
quit = False

while not quit:
    # compute time
    newTime = pygame.time.get_ticks() * 0.001
    deltaTime += newTime - oldTime
    oldTime = newTime
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit = True
        elif event.type == KEYDOWN:
            if event.key == K_a:
                spacecraft.angular_velocity = 2.0
            elif event.key == K_w:
                spacecraft.engine_force = 400000.0
            elif event.key == K_d:
                spacecraft.angular_velocity = -2.0
            elif event.key == K_ESCAPE:
                quit = True
        elif event.type == KEYUP:
            if event.key == K_a:
                spacecraft.angular_velocity = 0.0
            elif event.key == K_w:
                spacecraft.engine_force = 0.0
            elif event.key == K_d:
                spacecraft.angular_velocity = 0.0

    screen.fill((0, 0, 0))

    viewport = spacecraft.position - vec2(screen.get_size()) * 0.5
    background.on_redraw(screen, deltaTime, viewport)
    spacecraft.on_redraw(screen, deltaTime, viewport)
    for p in planets:
        p.on_redraw(screen, deltaTime, viewport)
    for a in asteroids:
        a.on_redraw(screen, deltaTime, viewport)
    for m in minerals:
        m.on_redraw(screen, deltaTime, viewport)
    # draw HUD
    pygame.draw.rect(screen, (255 - int(255 * fuel), 0, int(255 * fuel)), (0, screen.get_size()[1] - 20, int(fuel * 200), 20))
    pygame.draw.rect(screen, (255 - int(255 * health * health), int(255 * health), 0), (screen.get_size()[0] - int(health * 200), screen.get_size()[1] - 20, int(health * 200), 20))
    screen.blit(font.render("SCORE: " + str(score), True, (255, 255, 0)), (0, 0))
    drawVector(screen, vec2(48, 64), (minerals[-1].position - spacecraft.position).normal() * 32)
    pygame.display.update()

    # update state
    while deltaTime > TIME_STEP:
        # asteroids
        i, s = 0, len(asteroids)
        while i < s:
            if circleCircleCollide(asteroids[i].position, asteroids[i].radius, vec2(), ASTEROID_RADIUS + asteroids[i].radius):
                if collide(spacecraft, asteroids[i]):
                    spacecraft.position -= spacecraft.linear_velocity * TIME_STEP
                    asteroids[i].position -= asteroids[i].linear_velocity * TIME_STEP
                    normal = (asteroids[i].position - spacecraft.position).normal()
                    v0, u0 = project2(spacecraft.linear_velocity, normal)
                    v1, u1 = project2(asteroids[i].linear_velocity, normal)
                    alpha = spacecraft.mass - asteroids[i].mass
                    beta = spacecraft.mass + asteroids[i].mass
                    spacecraft.linear_velocity = u0 + v0 * alpha / beta + v1 * (2 * asteroids[i].mass / beta)
                    asteroids[i].linear_velocity = u1 + v1 * -alpha / beta + v0 * (2 * spacecraft.mass / beta)
                    health = max(0.0, health - (v0 + v1).length() * DAMAGE_FACTOR)
                asteroids[i].on_update(TIME_STEP)
                i += 1
            else:
                del asteroids[i]
                s -= 1

        # planets
        for p in planets:
            if collide(spacecraft, p):
                spacecraft.position -= spacecraft.linear_velocity * TIME_STEP
                normal = (p.position - spacecraft.position).normal()
                p, r = project2(spacecraft.linear_velocity, normal)
                health = max(0, health - p.length() * DAMAGE_FACTOR)
                spacecraft.linear_velocity = -reflect2(spacecraft.linear_velocity, normal)

        # minerals
        i, s = 0, len(minerals)
        while i < s:
            if collide(spacecraft, minerals[i]):
                score += minerals[i].index * 10
                if minerals[i].index == 0:
                    fuel = min(1.0, fuel + 0.33)
                del minerals[i]
                s -= 1
            else:
                i += 1

        # use fuel
        fuel = max(0.0, fuel - spacecraft.engine_force * FUEL_USAGE * TIME_STEP)
            
        spacecraft.external_force = getGravity(spacecraft, planets)
        spacecraft.on_update(TIME_STEP, newTime)
        if random() * TIME_STEP < ASTEROID_THRESHOLD:
            asteroids.append(drawAsteroid(planets))

        # game over
        if fuel == 0.0 or health == 0.0:
            game_over = font.render("GAME OVER", True, (255, 0, 0))
            position = (vec2(screen.get_size()) - vec2(game_over.get_size())) * 0.5
            screen.blit(game_over, position.intcpl())
            pygame.display.update()
            pygame.time.delay(3000)
            quit = True
            deltaTime = 0.0

        if minerals == []:
            game_over = bigfont.render("VICTORY", True, (0, 255, 0))
            position = (vec2(screen.get_size()) - vec2(game_over.get_size())) * 0.5
            screen.blit(game_over, position.intcpl())
            pygame.display.update()
            pygame.time.delay(3000)
            quit = True
            deltaTime = 0.0

        deltaTime -= TIME_STEP

