#!/home/larce/Documents/game1/game1_venv python

####

import configparser
import sys

import pygame
from loguru import logger
from perlin_noise import PerlinNoise

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
    def __init__(self, config, text, surfs):
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
        self.text = text
        self.surfs = surfs

    def run(self, mesh):
        """The mainloop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        mesh.freq_up()
                    if event.key == pygame.K_LEFT:
                        mesh.freq_down()
                    if event.key == pygame.K_r:
                        mesh.freq_reset()

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text(
                "FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                    self.clock.get_fps(), " " * 5, self.playtime
                ),
                (self.width),
                (self.height),
            )

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.paint(mesh(self.playtime))

        pygame.quit()