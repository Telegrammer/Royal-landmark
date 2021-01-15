from Physics import *
from Bullet import *
from Graphics import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, health, damage):
        super().__init__(Globals.all_sprites)
        self.add(Globals.player_group)
        self.image = pygame.transform.scale(load_image('player_stay_1.png', -1), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.falling = False
        self.jumping = False
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed_y = 10
        self.max_speed_x = 4
        self.god_mode_time = 0
        self.sphere_defence = 1
        self.health = health
        self.damage = damage
        self.run_frames = []
        self.current_frame = 0
        self.animation_run_delay = 0
        self.animation_stay_delay = 0
        for i in range(1, 4):
            self.run_frames.append(pygame.transform.scale(load_image(f'player_run_{i}.png', -1), (30, 30)))

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)
        gravity_work(self)
        collision_work(self)

        if self.jumping:
            self.image = pygame.transform.scale(load_image('player_fly.png', -1), (30, 30))
            try:
                assert self.speed_x < 0
                self.image = pygame.transform.flip(self.image, True, False)
            except AssertionError:
                pass
            self.current_frame = 0
        if self.speed_x != 0 and not self.falling and not self.jumping:
            self.image = self.run_frames[self.current_frame]
            try:
                assert self.speed_x < 0
                self.image = pygame.transform.flip(self.image, True, False)
            except AssertionError:
                pass
            try:
                assert not self.animation_run_delay
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.animation_run_delay = Globals.FPS // 50
            except AssertionError:
                self.animation_run_delay -= 1
        elif not self.falling and not self.jumping and not self.speed_x:
            self.animation_run_delay = 0
            try:
                assert not self.animation_stay_delay
                try:
                    assert not self.current_frame
                    self.current_frame = 1
                    self.animation_stay_delay = Globals.FPS
                except AssertionError:
                    self.animation_stay_delay = Globals.FPS // 30
                    self.current_frame = 0
                self.image = pygame.transform. \
                    scale(load_image(f'player_stay_{self.current_frame}.png', -1), (30, 30))
            except AssertionError:
                self.animation_stay_delay -= 1

        for hit_box in Globals.enemies_hit_boxes:
            try:
                assert pygame.sprite.collide_mask(hit_box, self) and not self.god_mode_time
                self.health -= 20
                self.check_death()
            except AssertionError:
                pass

        for bullet in Globals.enemy_bullets:
            try:
                assert pygame.sprite.collide_mask(bullet, self)
                Globals.enemy_bullets.remove(bullet)
                Globals.all_sprites.remove(bullet)
                assert not self.god_mode_time
                if type(bullet) == ShootarBullet or type(bullet) == MessyBullet:
                    self.health -= 20
                elif type(bullet) == BatMessyBullet:
                    self.health -= 15
                elif type(bullet) == ToorarBullet:
                    self.health -= 10
                else:
                    try:
                        assert Globals.stage_count < 8
                        self.health -= 25
                    except AssertionError:
                        self.health -= 50
                self.check_death()
            except AssertionError:
                pass

        try:
            assert self.god_mode_time
            self.god_mode_time -= 1
        except AssertionError:
            pass

    def check_death(self):
        try:
            assert self.health > 0
            self.god_mode_time = Globals.FPS * self.sphere_defence
        except AssertionError:
            self.health = 300
            self.damage = 35
            with open('data/character_save.txt', mode='w', encoding='utf8') as file:
                file.write('')
            with open('data/map.txt', mode='w', encoding='utf8') as file:
                file.write('')
            Globals.level_crossing = True
            Globals.pause = True
            Globals.enemies = pygame.sprite.Group()
            Globals.enemies_hit_boxes = []
            self.falling = True
