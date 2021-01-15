from Globals import *
from Graphics import load_image


class Part(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__(Globals.all_sprites, Globals.tiles)
        self.image = pygame.transform.scale(load_image(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class BackGroundPart(Part):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        Globals.tiles.remove(self)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos, image, level_door):
        super().__init__(Globals.all_sprites)
        self.image = pygame.transform.scale(load_image(image, colorkey=-1), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        try:
            assert level_door
            Globals.level_door.add(self)
        except AssertionError:
            pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(Globals.all_sprites, Globals.tiles)
        self.image = pygame.Surface([25, Globals.HEIGHT])
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
