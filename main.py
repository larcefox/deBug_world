#!/home/larce/Documents/game1/game1_venv python
 
"""
002_display_fps_pretty.py
 
Display framerate and playtime.
Works with Python 2.7 and 3.3+.
 
URL:     http://thepythongamebook.com/en:part2:pygame:step002
Author:  yipyip
License: Do What The Fuck You Want To Public License (WTFPL)
         See http://sam.zoy.org/wtfpl/
"""
 
####
 
import pygame
from perlin_noise import PerlinNoise
import configparser
import numpy as np
from loguru import logger
import sys


####

logger.add("log_file.log", colorize=True, format="{time} {level} <green>{message}</green>", level="INFO", rotation="5 MB")

####
 
config = configparser.ConfigParser()  # создаём объекта парсера
config.read('settings.ini')  # читаем конфиг

####
 
class Environment(object):
 
 
    def __init__(self, config, fps=30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("deBug World")
        self.width = int(config["Resolution"]["WIDTH"])
        self.height = int(config["Resolution"]["HEIGHT"])
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 10, bold=True)
        self.config = config
        self.frequency = 1
 
    def run(self, mesh):
        """The mainloop
        """
        mesh_original = mesh
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime), (self.width), (self.height))

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.paint(mesh)

        pygame.quit()
 
 
    def draw_text(self, text, pos_x, pos_y):
        """Center text in window
        """
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, (0, 255, 0))
        # // makes integer division in python3
        self.screen.blit(surface, (pos_x - fw, pos_y - fh))

    def paint(self, list_of_surfs): #TODO move all paint objects heare!
        """painting on the surface"""
        #------- try out some pygame draw functions --------
        # pygame.draw.line(Surface, color, start, end, width) 
        # pygame.draw.line(self.background, (0,255,0), (10,10), (50,100))
        # blits((source, dest, area), ...)) -> [Rect, ...]
        # self.screen.blits((tileImage, (centered_x, centered_y)))
        self.screen.blits(list_of_surfs)

 
####

class GameObject(object):
    def __init__(self, config, TILEWIDTH, TILEHEIGHT):
        self.config = config
        self.TILEWIDTH = TILEWIDTH  #holds the tile width and height
        self.TILEHEIGHT = TILEWIDTH
        self.TILEHEIGHT_HALF = self.TILEHEIGHT / 2
        self.TILEWIDTH_HALF = self.TILEWIDTH / 2
        
####

class Mesh(GameObject):
    def __init__(self, config, TILEWIDTH, TILEHEIGHT, evaluate):
        super().__init__(config, TILEWIDTH, TILEHEIGHT)
        self.evaluate = evaluate
        self.screen_x = int(config["Resolution"]["WIDTH"])
        self.screen_y = int(config["Resolution"]["HEIGHT"])
        self.bioms_dict = config["Bioms"]

    def __call__(self):

        bioms = self.load_bioms_from_cfg()
        list_of_surfs = []

        for row_nb, row in enumerate(self.evaluate):    #for every row of the map...
            for col_nb, tile in enumerate(row):    #for every cell of the map...
                DEEP = 50
                moisture = np.transpose(self.evaluate) # transponse matrix for moisture
                biom_name = self.mesh_img_chooser(self.evaluate[row_nb, col_nb], moisture[row_nb, col_nb])
                tileImage = bioms[biom_name]
                cart_x = row_nb * self.TILEWIDTH_HALF
                cart_y = col_nb * self.TILEHEIGHT_HALF  
                iso_x = (cart_x - cart_y) 
                iso_y = (cart_x + cart_y)/2
                centered_x = self.screen_x/2 + iso_x
                centered_y = self.screen_y/4 + iso_y
                centered_y = centered_y - (DEEP * self.evaluate[row_nb, col_nb]) - self.screen_x / 8
                # self.waving_ocean(playtime, col_nb, self.evaluate.shape, biom_name, DEEP) # waving ocean
                list_of_surfs.append((tileImage, (centered_x, centered_y)))

        return list_of_surfs

    # def waving_ocean(self, playtime, col_nb, mesh_shape, biom_name, deep):
    #     WAVE_HEIGHT = deep / 5
    #     wave_fraq = 100
    #     playtime = playtime * 10
    #     wave_num = int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq))
    #     PREV_WAVE = wave_num - 1
    #     NEXT_WAVE = wave_num + 1

    #     if biom_name == 'ocean':
    #         if int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq)) == col_nb:
    #             return WAVE_HEIGHT
    #         elif int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq)) == (col_nb + 1) and \
    #             col_nb < mesh_shape[0]:
    #             return WAVE_HEIGHT/2
    #         elif int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq)) == (col_nb - 1) and \
    #             col_nb > 0:
    #             return WAVE_HEIGHT/2

    #         elif int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq)) == (col_nb + 2) and \
    #             col_nb < mesh_shape[0]-1:
    #             return WAVE_HEIGHT/3
    #         elif int((mesh_shape[0]/wave_fraq) * (playtime % wave_fraq)) == (col_nb - 2) and \
    #             col_nb > 1:
    #             return WAVE_HEIGHT/3
    #     return 0    

    def load_bioms_from_cfg(self):
        bioms = {}
        for i in self.bioms_dict:
            bioms[i] = pygame.image.load(self.bioms_dict[i]).convert_alpha()
        return bioms

    def mesh_img_chooser(self, e, m):
        if (e < 0.1):
            logger.info(f"Eval: {e}, mois: {m}, ocean")
            return 'ocean'

        elif (e > 0.8):
            if (m < 0.1):
                return 'scorched'
            elif (m < 0.2):
                return 'bare'
            elif (m < 0.5):
                return 'tundra'
            return 'snow'

        elif (e > 0.6):
            if (m < 0.33):
                return 'temperate_desert'
            elif (m < 0.66):
                return 'shrubland'
            return 'taiga'

        elif (e > 0.3):
            if (m < 0.16):
                return 'temperate_desert'
            elif (m < 0.50):
                return 'grassland'
            elif (m < 0.83):
                return 'temperate_deciduous_forest'
            return 'temperate_rain_forest'

        elif (m < 0.16):
            return 'subtropical_desert'
        elif (m < 0.33):
            return 'grassland'
        elif (m < 0.66):
            return 'tropical_seasonal_forest'

        return 'tropical_rain_forest'

####

class MatrixGenerator(object):
    
        def __init__(self, width, height, power=1, frequency=1, move=1):
            '''Main class for all game meshes
            '''
            self.width = width
            self.height = height
            self.power = power
            self.frequency = frequency
            self.move = move
            self.noise = PerlinNoise(octaves=10)

        def __call__(self):
            return np.array([[self.noise([i/self.width, j/self.height]) for j in range(self.width)] for i in range(self.height)])

        
####
 
if __name__ == '__main__':
 
    # call with width of window and fps
    game = Environment(config)
    matrix = MatrixGenerator(100, 100)
    mesh = Mesh(config, 16, 16, matrix())
    game.run(mesh())