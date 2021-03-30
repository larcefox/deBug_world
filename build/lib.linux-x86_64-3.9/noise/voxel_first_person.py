#!/home/larce/Documents/game1/game1_venv/bin/python

####

import configparser
import sys

import numpy as np
from loguru import logger
from perlin_noise import PerlinNoise
import ursina as ua
from ursina.prefabs.first_person_controller import FirstPersonController


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


app = ua.Ursina()
ua.window.borderless = False
#ua.window.fps_counter.enabled = False
ua.window.exit_button.visible = False
####


class Environment(object):
    def __init__(self, config):
        self.screen = ua.window
        self.config = config
        self.TILEWIDTH = float(
            config["TILESIZE"]["TILEWIDTH"]
        )  # holds the tile width and height
        self.TILEHEIGHT = float(config["TILESIZE"]["TILEHEIGHT"])
        self.TILEHEIGHT_HALF = self.TILEHEIGHT / 2
        self.TILEWIDTH_HALF = self.TILEWIDTH / 2
        self.evaluate = MatrixGenerator(config)() # eval matrix
        self.original_eval = self.evaluate # seve original eval matrix
        self.screen_x = int(config["SCREEN"]["WIDTH"])
        self.screen_y = int(config["SCREEN"]["HEIGHT"])
        self.screen.size = (self.screen_x, self.screen_y)
        self.bioms_dict = config[f"Bioms_64x64"]
        self.moisture = np.transpose(self.evaluate)  # transponse matrix for moisture
        self.DEEP = int(config["MeshParam"]["MAX_DEEP"])
        
        self.texture_dict = {i:ua.load_texture(self.bioms_dict[i]) for i in self.bioms_dict}

    def draw(self):  
        for row_nb, row in enumerate(self.evaluate):  # for every row of the map...
            for col_nb, tile in enumerate(row):  # for every cell of the map...
                biom_name = self.mesh_img_chooser(
                    self.evaluate[row_nb, col_nb], self.moisture[row_nb, col_nb]
                )
                texture = self.texture_dict[biom_name]
                cart_x = row_nb * self.TILEWIDTH / 1.5
                cart_z = col_nb * self.TILEHEIGHT / 1.5
                iso_x = cart_x - cart_z
                iso_z = (cart_x + cart_z)
                pos_x = iso_x
                pos_z = iso_z
                pos_y = self.DEEP * self.evaluate[row_nb, col_nb]
                #pos_y = (pos_y - (self.DEEP * self.evaluate[row_nb, col_nb]) - self.screen_x / 8)
                #ua.Entity(model="quad", texture = texture, scale=(self.TILEWIDTH,self.TILEHEIGHT), position=(pos_x,pos_y))
                ua.Entity(
                    model="cube",
                    texture=texture, 
                    rotation=(0,45,0), 
                    scale=(self.TILEWIDTH, self.TILEHEIGHT, (self.TILEWIDTH + self.TILEHEIGHT)/2), 
                    position=(pos_x, pos_y, pos_z), 
                    parent=ua.scene,
                    collision=True,
                    collider = 'box' 
                    )
                #logger.info((pos_x, pos_y, pos_z))        
                

    
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

if __name__ == "__main__":

    # call with width of window and fps
    game = Environment(config)
    game.draw()
   
    player = FirstPersonController()

    def update():
        pass
    #     if (ua.held_keys['w']):
    #         ua.camera.rotation_x -= 1
    #     if (ua.held_keys['s']):
    #         ua.camera.rotation_x += 1

    #     if (ua.held_keys['q']):
    #         ua.camera.rotation_y -= 1
    #     if (ua.held_keys['e']):
    #         ua.camera.rotation_y += 1

    #     if (ua.held_keys['d']):
    #         ua.camera.rotation_z += 1
    #     if (ua.held_keys['a']):
    #         ua.camera.rotation_z -= 1
    #     # logger.info(ua.camera.position)

    #     # 'up arrow': 0, 'shift': 0, 'right arrow': 0, 'left arrow': 0, 'down arrow': 0})

    #     if (ua.held_keys['8']):
    #         ua.camera.position += ua.Vec3(0, 1, 0)
    #     if (ua.held_keys['5']):
    #         ua.camera.position += ua.Vec3(0, -1, 0)

    #     if (ua.held_keys['6']):
    #         ua.camera.position += ua.Vec3(1, 0, 0)
    #     if (ua.held_keys['4']):
    #         ua.camera.position += ua.Vec3(-1, 0, 0)

    #     if (ua.held_keys['7']):
    #         ua.camera.position += ua.Vec3(0, 0, 1)
    #     if (ua.held_keys['9']):
    #         ua.camera.position += ua.Vec3(0, 0, -1)
    #     logger.info(ua.camera.position)
    # ua.camera.position = (50, 10, 80)

    app.run()
    