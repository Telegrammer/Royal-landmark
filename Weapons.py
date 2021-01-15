import pygame
from Globals import Globals
from Graphics import load_image
from math import atan2, pi


class Bow(pygame.sprite.Sprite):
    def __init__(self, rect, damage):
        super().__init__(Globals.all_sprites, Globals.player_group)
        self.image = pygame.transform.scale(load_image('sphere_of_protection.png'), (rect[2], rect[3]))
        self.original_image = self.image
        self.rect = pygame.Rect(rect)

        self.angle = 0
        self.damage = damage

    def update(self, pos):
        try:
            assert pos[0] < pygame.mouse.get_pos()[0]
            self.rect.x = pos[0] + 10
        except AssertionError:
            self.rect.x = pos[0] - 30
        try:
            assert pos[1] < pygame.mouse.get_pos()[1]
            self.rect.y = pos[1] + 10
        except AssertionError:
            self.rect.y = pos[1] - 30

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        vector_x, vector_y = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        self.angle = -(atan2(vector_x, vector_y) * 180 / pi)
        self.image = pygame.transform.rotate(self.original_image, -int(self.angle) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
