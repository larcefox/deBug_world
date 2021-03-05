#!/home/larce/Documents/game1/game1_venv/bin/python

####

import configparser
import sys

import numpy as np
import pygame
from loguru import logger
from perlin_noise import PerlinNoise
from classes.game_sprites import ConcreteSpriteFactory


####

logger.add(
    "log_file.log",
    colorize=True,
    format="{time} {level} <green>{message}</green>",
    level="INFO",
    rotation="5 MB",
)

####

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

####


class Environment(object):
    def __init__(self, config):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        pygame.display.set_caption(config["CAPTION"]["TEXT"])
        self.width = int(config["SCREEN"]["WIDTH"])
        self.height = int(config["SCREEN"]["HEIGHT"])
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF
        )
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = int(config["SCREEN"]["FPS"])
        self.playtime = 0.0
        self.font = pygame.font.SysFont(
            config["FONTS"]["STANDART_NAME"], 
            int(config["FONTS"]["STANDART_SIZE"]), 
            config["FONTS"]["OPT"]
            )
        self.config = config
        self.running = True
        
    def control(self, event):
        if event.type == pygame.QUIT: 
            self.running = False
            #logger.info(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mesh.freq_up()
                mesh_sprite_groups = mesh.get_group()
            if event.key == pygame.K_LEFT:
                mesh.freq_down()
                mesh_sprite_groups = mesh.get_group()
            if event.key == pygame.K_r:
                mesh.freq_reset()
                mesh_sprite_groups = mesh.get_group()

    def run(self, mesh, dict_of_sprite_objects):
        """The mainloop"""
        dict_of_sprite_groups = mesh.get_group()
        while self.running:
            for event in pygame.event.get():
                self.control(event)
                
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            
            self.screen.blit(self.background, (0, 0))
            #self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(self.clock.get_fps(), " " * 5, self.playtime), (self.width), (self.height),)

            hwt = dict_of_sprite_objects['text'](
                "FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format( self.clock.get_fps(), " " * 5, self.playtime),
                self.width,
                self.height,
                size=20
                )
            
            [dict_of_sprite_groups[i].draw(self.screen) for i in dict_of_sprite_groups]
            self.screen.blit(hwt.image, hwt.rect)

            #mesh_sprite_groups['ocean'].clear(self.screen, self.background)

            pygame.display.flip()

        pygame.quit()


####


class MeshSpriteGroup():

    def __init__(self, config):
        self.config = config
        self.TILEWIDTH = int(
            config["TILESIZE"]["TILEWIDTH"]
        )  # holds the tile width and height
        self.TILEHEIGHT = int(config["TILESIZE"]["TILEHEIGHT"])
        self.TILEHEIGHT_HALF = self.TILEHEIGHT / 2
        self.TILEWIDTH_HALF = self.TILEWIDTH / 2
        self.freq = 1 # level of hight
        self.evaluate = MatrixGenerator(config)() # eval matrix
        self.original_eval = self.evaluate # seve original eval matrix
        self.screen_x = int(config["SCREEN"]["WIDTH"])
        self.screen_y = int(config["SCREEN"]["HEIGHT"])
        self.bioms_dict = config[
            f"Bioms_{config['TILESIZE']['TILEWIDTH']}x{config['TILESIZE']['TILEHEIGHT']}"
        ]
        self.moisture = np.transpose(self.evaluate)  # transponse matrix for moisture
        self.DEEP = int(config["MeshParam"]["MAX_DEEP"])
        self.sprite_groups_dict = {i:pygame.sprite.Group() for i in config[f"Bioms_{config['TILESIZE']['TILEWIDTH']}x{config['TILESIZE']['TILEHEIGHT']}"]}
        
    def get_group(self):
        [pygame.sprite.Group.empty(self.sprite_groups_dict[i]) for i in self.sprite_groups_dict]
        
        for row_nb, row in enumerate(self.evaluate):  # for every row of the map...
            for col_nb, tile in enumerate(row):  # for every cell of the map...
                biom_name = self.mesh_img_chooser(
                    self.evaluate[row_nb, col_nb], self.moisture[row_nb, col_nb]
                )
                filename = self.bioms_dict[biom_name]
                cart_x = row_nb * self.TILEWIDTH_HALF
                cart_y = col_nb * self.TILEHEIGHT_HALF
                iso_x = cart_x - cart_y
                iso_y = (cart_x + cart_y) / 2
                pos_x = self.screen_x / 2 + iso_x
                pos_y = self.screen_y / 4 + iso_y
                pos_y = (
                    pos_y
                    - (self.DEEP * self.evaluate[row_nb, col_nb])
                    - self.screen_x / 8)

                self.sprite_groups_dict[biom_name].add(ConcreteSpriteFactory.create_game_sprite(filename, pos_x, pos_y))
                
        return self.sprite_groups_dict

    def waving_ocean(self, playtime, col_nb, mesh_shape, biom_name, deep):
        WAVE_HEIGHT = deep / 5
        wave_fraq = 100
        playtime = playtime * 10
        wave_num = int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq))
        PREV_WAVE = wave_num - 1
        NEXT_WAVE = wave_num + 1

        if biom_name == "ocean":
            if int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq)) == col_nb:
                return WAVE_HEIGHT
            elif (
                int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq))
                == (col_nb + 1)
                and col_nb < mesh_shape[0]
            ):
                return WAVE_HEIGHT / 2
            elif (
                int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq))
                == (col_nb - 1)
                and col_nb > 0
            ):
                return WAVE_HEIGHT / 2

            elif (
                int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq))
                == (col_nb + 2)
                and col_nb < mesh_shape[0] - 1
            ):
                return WAVE_HEIGHT / 3
            elif (
                int((mesh_shape[0] / wave_fraq) * (playtime % wave_fraq))
                == (col_nb - 2)
                and col_nb > 1
            ):
                return WAVE_HEIGHT / 3
        return 0

    def mesh_img_chooser(self, e, m):
        if e < 0.1:
            return "ocean"

        elif e > 0.8:
            if m < 0.1:
                return "scorched"
            elif m < 0.2:
                return "bare"
            elif m < 0.5:
                return "tundra"
            return "snow"

        elif e > 0.6:
            if m < 0.33:
                return "temperate_desert"
            elif m < 0.66:
                return "shrubland"
            return "taiga"

        elif e > 0.3:
            if m < 0.16:
                return "temperate_desert"
            elif m < 0.50:
                return "grassland"
            elif m < 0.83:
                return "temperate_deciduous_forest"
            return "temperate_rain_forest"

        elif m < 0.16:
            return "subtropical_desert"
        elif m < 0.33:
            return "grassland"
        elif m < 0.66:
            return "tropical_seasonal_forest"

        return "tropical_rain_forest"

    def freq_up(self):
        self.freq += 0.1
        self.evaluate = self.original_eval * self.freq

    def freq_down(self):
        self.freq -= 0.1
        self.evaluate = self.original_eval * self.freq

    def freq_reset(self):
        self.freq = 1
        self.evaluate = self.original_eval
        

####


class MatrixGenerator(object):
    def __init__(self, config, power=1, frequency=1, move=1):
        """Main class for all game meshes"""
        self.width = int(config["MeshParam"]["WIDTH"])
        self.height = int(config["MeshParam"]["HEIGHT"])
        self.power = power
        self.frequency = frequency
        self.move = move
        self.noise = PerlinNoise(octaves=10)

    def __call__(self):
        return np.array(
            [
                [
                    self.noise([i / self.width, j / self.height])
                    for j in range(self.width)
                ]
                for i in range(self.height)
            ]
        )

####

dict_of_sprite_objects = {
    'text':ConcreteSpriteFactory.create_text,
                            }

####

if __name__ == "__main__":

    # call with width of window and fps
    game = Environment(config)
    mesh = MeshSpriteGroup(config)
    game.run(mesh, dict_of_sprite_objects)
