import numpy as np
import pygame
from pygame import gfxdraw
from perlin import perlin_list
import configparser  # импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read('settings.ini')  # читаем конфиг

power = 1
frequency = 1
movement = 1
resolution = width, height = 14, 14

evaluate_original = evaluate = perlin_list(width, height)
moisture = perlin_list(width, height)

screen = pygame.display.set_mode((resolution))
clock = pygame.time.Clock()
FPS = 30  # Frames per second.

def biome(e, m):
    if (e < 0.1):
        return 'OCEAN'

    if (e > 0.8):
        if (m < 0.1):
            return 'SCORCHED'
        if (m < 0.2):
            return 'BARE'
        if (m < 0.5):
            return 'TUNDRA'
        return 'SNOW'

    if (e > 0.6):
        if (m < 0.33):
            return 'TEMPERATE_DESERT'
        if (m < 0.66):
            return 'SHRUBLAND'
        return 'TAIGA'

    if (e > 0.3):
        if (m < 0.16):
            return 'TEMPERATE_DESERT'
        if (m < 0.50):
            return 'GRASSLAND'
        if (m < 0.83):
            return 'TEMPERATE_DECIDUOUS_FOREST'
        return 'TEMPERATE_RAIN_FOREST'

    if (m < 0.16):
        return 'SUBTROPICAL_DESERT'
    if (m < 0.33):
        return 'GRASSLAND'
    if (m < 0.66):
        return 'TROPICAL_SEASONAL_FOREST'
    return 'TROPICAL_RAIN_FOREST'

while True:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                power += 0.1
                evaluate = evaluate_original ** power                
            elif event.key == pygame.K_RIGHT:
                power -= 0.1
                evaluate = evaluate_original ** power
            elif event.key == pygame.K_UP:
                frequency += 0.1
                evaluate = evaluate_original * frequency
            elif event.key == pygame.K_DOWN:
                frequency -= 0.1
                evaluate = evaluate_original * frequency
            elif event.key == pygame.K_c:
                evaluate = evaluate_original

    # screen.fill(pygame.Color(SNOW), ((360, 239), (1, 1)))
    # screen.set_at((360, 241), pygame.Color(SNOW))
    # screen.set_at((360, 240), pygame.Color(SNOW))
    # screen.set_at((360, 239), pygame.Color(SNOW))
    #gfxdraw.pixel(screen, 360, 239, pygame.Color(config["Colors"]["SNOW"]))

    for row in range(height):
        for pix in range(width):
            gfxdraw.pixel(screen, pix, row, pygame.Color(config["Colors"][biome(evaluate[row, pix], moisture[row, pix])]))

    pygame.display.update()