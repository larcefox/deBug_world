from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


class DeBugSprite(type, pygame.sprite.Sprite):
    def __init__(self, filename, pos_x, pos_y):
        super().__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos_x = pos_x
        self.pos_y = pos_y


    def update(self):
        pass



class AbstractSpriteFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_mesh(self) -> AbstractMesh:
        pass


class ConcreteSpriteFactory(AbstractSpriteFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """

    def create_mesh(filename, pos_x, pos_y) -> Mesh:
        return Mesh(filename, pos_x, pos_y)



class Mesh(pygame.sprite.Sprite):

    def __init__(self, filename, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        pass
