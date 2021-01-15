import os
import sys

from Globals import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(Globals.all_sprites, Globals.health_bars)
        self.image = pygame.Surface([width, height])

        self.image.fill(pygame.color.Color('cyan'))
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 10

    def update(self, character):
        self.image = pygame.Surface([self.rect.width / (self.rect.width / character.health), self.rect.height])
        self.image.fill(pygame.color.Color('cyan'))


class Certain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Globals.all_sprites, Globals.certain)
        self.transparency = 255
        self.image = pygame.Surface([Globals.WIDTH, Globals.HEIGHT])
        self.image.fill(pygame.color.Color('black'))
        self.image.set_alpha(self.transparency)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
