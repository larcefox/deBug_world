from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
import math

class AbstractSpriteFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_mesh(self) -> Mesh:
        pass


class ConcreteSpriteFactory(AbstractSpriteFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """

    def create_game_sprite(filename, pos_x, pos_y) -> GameSprite:
        return GameSprite(filename, pos_x, pos_y)

    def create_text(text, pos_x, pos_y, font_name=None, size=20, color=(0,255,200)) -> Text:
        return Text(text, pos_x, pos_y, font_name, size, color)




class GameSprite(pygame.sprite.Sprite):

    def __init__(self, filename, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.temp_pos_y = pos_y
    def update(self, play_time):
        self.pos_y = self.temp_pos_y * math.sin(play_time)

class Text(pygame.sprite.Sprite):
    """ a helper class to write text on the screen """
    number = 0 
    book = {}
    def __init__(self, text, pos_x, pos_y, font_name, size, color):
        self.number = Text.number # get a unique number
        Text.number += 1 # prepare number for next Textsprite
        Text.book[self.number] = self # store myself into the book
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.changemsg(text, pos_x, pos_y, font_name, size, color)
         
    def update(self, seconds):        
        pass
         
    def changemsg(self, text, pos_x, pos_y, font_name=None, size=20, color=(0,255,100)):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.font = pygame.font.Font(font_name,size)
        fw, fh = self.font.size(text)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos_x - fw
        self.rect.centery = self.pos_y - fh