import pygame
from pygame.locals import *
import sys
from perlin import perlin_list
import configparser  # импортируем библиотеку
 
config = configparser.ConfigParser()  # создаём объекта парсера
config.read('settings.ini')  # читаем конфиг

power = 1
frequency = 1
movement = 1
resolution = width, height = 300, 300

evaluate_original = evaluate = perlin_list(width, height)
moisture = perlin_list(width, height)

def biome(e, m):
    if (e < 0.1):
        return 'ocean'

    if (e > 0.8):
        if (m < 0.1):
            return 'scorched'
        if (m < 0.2):
            return 'bare'
        if (m < 0.5):
            return 'tundra'
        return 'snow'

    if (e > 0.6):
        if (m < 0.33):
            return 'temperate_desert'
        if (m < 0.66):
            return 'shrubland'
        return 'taiga'

    if (e > 0.3):
        if (m < 0.16):
            return 'temperate_desert'
        if (m < 0.50):
            return 'grassland'
        if (m < 0.83):
            return 'temperate_deciduous_forest'
        return 'temperate_rain_forest'

    if (m < 0.16):
        return 'subtropical_desert'
    if (m < 0.33):
        return 'grassland'
    if (m < 0.66):
        return 'tropical_seasonal_forest'
    return 'tropical_rain_forest'

pygame.init()
 
DISPLAYSURF = pygame.display.set_mode((1100, 700), DOUBLEBUF)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()
 
map_data = evaluate      #the data for the map expressed as [row[tile]].
 
# wall = pygame.image.load('wall.png').convert_alpha()  #load images
# grass = pygame.image.load('grass.png').convert_alpha()

bioms = {}
for i in config["Bioms"]:
    bioms[i] = pygame.image.load(config["Bioms"][i]).convert_alpha()
    

TILEWIDTH = 64  #holds the tile width and height
TILEHEIGHT = 64
TILEHEIGHT_HALF = TILEHEIGHT /2
TILEWIDTH_HALF = TILEWIDTH /2
 
def load_surfs(map_data):
    for row_nb, row in enumerate(map_data):    #for every row of the map...
        for col_nb, tile in enumerate(row):    #for every cell of the map...

            tileImage = bioms[biome(evaluate[row_nb, col_nb], moisture[row_nb, col_nb])]

            cart_x = row_nb * TILEWIDTH_HALF
            cart_y = col_nb * TILEHEIGHT_HALF  
            iso_x = (cart_x - cart_y) 
            iso_y = (cart_x + cart_y)/2
            centered_x = DISPLAYSURF.get_rect().centerx + iso_x
            centered_y = DISPLAYSURF.get_rect().centery/2 + iso_y
            DISPLAYSURF.blit(tileImage, (centered_x, centered_y)) #display the actual tile

load_surfs(map_data)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:
                power += 0.1
                evaluate = evaluate_original ** power                
            if event.key == pygame.K_RIGHT:
                power -= 0.1
                evaluate = evaluate_original ** power
            if event.key == pygame.K_UP:
                frequency += 0.1
                evaluate = evaluate_original * frequency
            if event.key == pygame.K_DOWN:
                frequency -= 0.1
                evaluate = evaluate_original * frequency
            if event.key == pygame.K_c:
                evaluate = evaluate_original
                
    pygame.display.flip()
    FPSCLOCK.tick(30)