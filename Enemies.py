from random import randrange
from math import atan2, pi

from Physics import gravity_work, collision_work
from Bullet import *


class HitBox(pygame.sprite.Sprite):
    def __init__(self, pos, sheet, columns, rows, health):
        super(HitBox, self).__init__(Globals.all_sprites)
        self.frames = []
        self.animation_delay = 0
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(pos[0], pos[1] + 1, 30, 30)
        self.health = health
        if Globals.stage_count:
            self.health = self.health * round(1.1 * Globals.stage_count)
        Globals.enemies_hit_boxes.append(self)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (30, 30)))

    def animation_update(self):
        try:
            assert not self.animation_delay
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            pos = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
        except AssertionError:
            pass


class Shootar(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super(Shootar, self).__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.fire_delay = 0
        self.bullets_count = Globals.stage_count // 4 + 1

    def update(self, character):
        try:
            assert not self.fire_delay
            target_pos = character.rect.center
            vector_x, vector_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            angle = -(atan2(vector_x, vector_y) * 180 / pi) + randrange(-6, 6)
            try:
                assert self.bullets_count
                ShootarBullet(self.rect.center, angle, 'enemy_bullet.png')
                self.bullets_count -= 1
                self.fire_delay = Globals.FPS // 4
            except AssertionError:
                self.bullets_count = Globals.stage_count // 4 + 1
                self.fire_delay = Globals.FPS * 2
        except AssertionError:
            self.fire_delay -= 1
        try:
            assert not self.animation_delay
            self.animation_update()
            self.animation_delay = Globals.FPS
        except AssertionError:
            self.animation_delay -= 1


class Messy(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.fire_delay = 0
        self.bullets_count = Globals.stage_count // 4 + 1

    def update(self, character):
        try:
            assert not self.fire_delay
            target_pos = character.rect.center
            vector_x, vector_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            angle = -(atan2(vector_x, vector_y) * 180 / pi) + randrange(-6, 6)
            try:
                assert self.bullets_count
                MessyBullet(self.rect.center, angle + 15, 'enemy_bullet.png')
                MessyBullet(self.rect.center, angle - 15, 'enemy_bullet.png')
                try:
                    assert Globals.stage_count > 8
                    MessyBullet(self.rect.center, angle, 'enemy_bullet.png')
                except AssertionError:
                    pass
                self.bullets_count -= 1
                self.fire_delay = Globals.FPS // 4
            except AssertionError:
                self.bullets_count = Globals.stage_count // 4 + 1
                self.fire_delay = Globals.FPS * 2
                self.fire_delay = Globals.FPS
        except AssertionError:
            self.fire_delay -= 1
        try:
            assert not self.animation_delay
            self.animation_update()
            self.animation_delay = Globals.FPS + randrange(0, 20)
        except AssertionError:
            self.animation_delay -= 1


class Bat(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.acceleration = randrange(1, 4) * 0.1
        self.speed_x = randrange(0, 1)
        self.max_speed_x = randrange(5, 7)
        self.max_speed_y = 0

    def update(self, *args):
        self.rect = self.rect.move(self.speed_x, 0)
        collision_work(self)
        try:
            assert self.speed_x == 0 or \
                   (self.speed_x >= self.max_speed_x or self.speed_x <= -self.max_speed_x)
            self.acceleration = -self.acceleration
        except AssertionError:
            pass
        self.speed_x += self.acceleration
        try:
            assert not self.animation_delay
            self.animation_update()
            try:
                assert self.acceleration > 0
                self.image = pygame.transform.flip(self.image, True, False)
            except AssertionError:
                pass
            self.animation_delay = Globals.FPS // 10 + randrange(-1, 1)
        except AssertionError:
            self.animation_delay -= 1


class BatMessy(Bat):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        self.fire_delay = 0

    def update(self, character):
        super(BatMessy, self).update(character)
        try:
            assert not self.fire_delay
            target_pos = character.rect.center
            vector_x, vector_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            angle = -(atan2(vector_x, vector_y) * 180 / pi) + randrange(-6, 6)
            BatMessyBullet(self.rect.center, angle + 15, 'enemy_bullet.png')
            BatMessyBullet(self.rect.center, angle - 15, 'enemy_bullet.png')
            try:
                assert Globals.stage_count > 6
                BatMessyBullet(self.rect.center, 90, 'enemy_bullet.png')
                BatMessyBullet(self.rect.center, -90, 'enemy_bullet.png')
            except AssertionError:
                pass
            self.fire_delay = Globals.FPS
        except AssertionError:
            self.fire_delay -= 1


class Winger(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.acceleration = randrange(1, 4) * 0.1
        self.speed_y = randrange(0, 1)
        self.max_speed_y = randrange(5, 7)
        self.max_speed_x = 0

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed_y)
        collision_work(self)
        try:
            assert self.speed_y == 0 or \
                   (self.speed_y >= self.max_speed_y or self.speed_y <= -self.max_speed_y)
            self.acceleration = -self.acceleration
        except AssertionError:
            pass
        self.speed_y += self.acceleration
        try:
            assert not self.animation_delay
            self.animation_update()
            try:
                assert self.acceleration > 0
                self.image = pygame.transform.flip(self.image, True, False)
            except AssertionError:
                pass
            self.animation_delay = Globals.FPS // 10
        except AssertionError:
            self.animation_delay -= 1


class Toorar(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.fire_delay = 0
        self.choice = randrange(-2, 5)
        self.angle = randrange(0, 15)

    def update(self, *args):
        self.animation_update()
        try:
            assert not self.fire_delay
            ToorarBullet(self.rect.center, self.angle + randrange(-6, 6),
                         'enemy_bullet.png')
            try:
                assert Globals.stage_count >= 12
                ToorarBullet(self.rect.center, -(self.angle + randrange(-6, 6)),
                             'enemy_bullet.png')
            except AssertionError:
                pass
            self.fire_delay = Globals.FPS * 0.1
            try:
                assert self.angle >= 360
                self.angle = randrange(0, 15)
            except AssertionError:
                try:
                    assert self.choice
                    self.angle += 15
                except AssertionError:
                    self.angle -= 15
        except AssertionError:
            self.fire_delay -= 1


class BrokenToorar(HitBox):
    def __init__(self, pos, sheet, columns, rows, health):
        super().__init__(pos, sheet, columns, rows, health)
        Globals.enemies.add(self)

        self.fire_delay = 0

    def update(self, *args):
        try:
            assert not self.fire_delay
            BrokenToorarBullet(self.rect.center, randrange(0, 360), 'enemy_bullet.png')
            self.fire_delay = randrange(Globals.FPS // 6, Globals.FPS * 2)
        except AssertionError:
            self.fire_delay -= 1
        try:
            assert not self.animation_delay
            self.animation_update()
            self.animation_delay = Globals.FPS
        except AssertionError:
            self.animation_delay -= 1
