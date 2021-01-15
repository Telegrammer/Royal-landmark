import pygame
from pygame.math import Vector2
from Globals import Globals
from Graphics import load_image

BULLET_IMAGE = pygame.Surface((20, 11), pygame.SRCALPHA)
pygame.draw.polygon(BULLET_IMAGE, pygame.Color('aquamarine1'),
                    [(0, 0), (20, 5), (0, 11)])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, image):
        super().__init__(Globals.all_sprites)
        Globals.player_bullets.add(self)

        self.image = pygame.transform.rotate(load_image(image, -1), -(angle + 90))
        self.rect = self.image.get_rect(center=pos)
        offset = Vector2(0, 0).rotate(angle + 90)
        self.pos = Vector2(pos) + offset
        self.velocity = Vector2(1, 0).rotate(angle + 90) * (Globals.FPS / 9)

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos


class ShootarBullet(Bullet):
    def __init__(self, pos, angle, image):
        super().__init__(pos, angle, image)
        Globals.player_bullets.remove(self)
        Globals.enemy_bullets.add(self)


class MessyBullet(Bullet):
    def __init__(self, pos, angle, image):
        super().__init__(pos, angle, image)
        Globals.player_bullets.remove(self)
        Globals.enemy_bullets.add(self)


class BatMessyBullet(Bullet):
    def __init__(self, pos, angle, image):
        super().__init__(pos, angle, image)
        Globals.player_bullets.remove(self)
        Globals.enemy_bullets.add(self)


class ToorarBullet(Bullet):
    def __init__(self, pos, angle, image):
        super().__init__(pos, angle, image)
        Globals.player_bullets.remove(self)
        Globals.enemy_bullets.add(self)


class BrokenToorarBullet(Bullet):
    def __init__(self, pos, angle, image):
        super().__init__(pos, angle, image)
        Globals.player_bullets.remove(self)
        Globals.enemy_bullets.add(self)
