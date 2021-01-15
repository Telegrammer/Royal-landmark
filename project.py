from random import randrange

from Bullet import Bullet
from Graphics import *
from Physics import bullet_physics
from Player import Player
from Tiles import *
from Weapons import *
from map import MapGenerator, generate

pygame.init()
pygame.display.set_caption("Build 99")
screen = pygame.display.set_mode(Globals.SIZE)
clock = pygame.time.Clock()
new_level = False

'''
generate_level - это функция, которая вызывает рисование карты

main_function - это основная функция программы, которая запускает саму программу

class menu - это меню программы
'''


def generate_level():
    level = MapGenerator(Globals.level_base).return_map()
    generate(level)


# ----------------------------- Основная функция ---------------------------

def main_function():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Globals.game_cycle = False
            if event.type == pygame.MOUSEBUTTONDOWN and not Globals.pause:
                if event.button == 1 and len(Globals.player_bullets) < 6:
                    Bullet(bow.rect.center, bow.angle, 'player_bullet.png')

        if Globals.object_appearance:
            certain.transparency -= 5
            if certain.transparency <= 0:
                Globals.pause = False
                Globals.object_appearance = False
                certain.transparency = 0
            certain.image.set_alpha(certain.transparency)
            Globals.all_sprites.draw(screen)
            Globals.certain.draw(screen)

        if pygame.key.get_pressed():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and not Globals.object_appearance:
                Menu('Продолжить игру')
            if keys[pygame.K_a]:
                player.speed_x = -player.max_speed_x
            elif keys[pygame.K_d]:
                player.speed_x = player.max_speed_x
            if keys[pygame.K_SPACE] and not player.jumping and not player.falling:
                player.jumping = True

        if not Globals.pause:
            player.update()
            Globals.enemies.update(player)
            bow.update(player.rect.center)

            Globals.player_bullets.update()
            Globals.enemy_bullets.update()

            Globals.health_bars.update(player)

            bullet_physics(player)

            player.speed_x = 0
        screen.fill((0, 0, 0))
        clock.tick(Globals.FPS)
        Globals.all_sprites.draw(screen)
        Globals.health_bars.draw(screen)
        Globals.player_group.draw(screen)
        Globals.certain.draw(screen)
        pygame.display.flip()

        if pygame.sprite.spritecollideany(player, Globals.level_door) and \
                not Globals.enemies_hit_boxes and not Globals.pause:
            Globals.level_crossing = True
            Globals.pause = True
            Globals.level_count += 1
            if Globals.level_count == 5:
                Globals.level_count = 0
                Globals.stage_count += 1
                print(Globals.stage_count)
                if player.health < 100:
                    player.health = 300
                    Globals.health_bars.update(player)
                else:
                    choice = randrange(0, 5)
                    if not choice:
                        player.sphere_defence += 1
                    else:
                        player.damage += randrange(7, 17)

        if Globals.level_crossing:
            certain.transparency += 5
            certain.image.set_alpha(certain.transparency)
            if certain.transparency == 255:
                for sprite in Globals.all_sprites:
                    if sprite == player:
                        player.rect.x, player.rect.y = 50, 540
                    elif sprite == bow:
                        bow.update(player.rect.center)
                    elif sprite == certain:
                        pass
                    else:
                        Globals.all_sprites.remove(sprite)
                Globals.tiles = pygame.sprite.Group()
                Globals.level_door = pygame.sprite.Group()
                Globals.player_bullets = pygame.sprite.Group()
                Globals.enemy_bullets = pygame.sprite.Group()
                running = False
                Globals.level_crossing = False
                Globals.object_appearance = True


# ---------------------------- Класс меню ----------------------------------

class Menu:
    def __init__(self, text):
        import pygame_gui
        pygame.init()
        pygame.display.set_caption('Quick Start')
        window_surface = pygame.display.set_mode((600, 600))

        background = pygame.image.load("data/back_menu.png")

        manager = pygame_gui.UIManager((600, 600), 'theme.json')

        begin_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 255), (250, 50)),
                                                 text=text,
                                                 manager=manager)

        exit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 340), (250, 50)),
                                                text='Выйти из игры',
                                                manager=manager)
        if Globals.game_cycle:
            pygame_gui.elements.ui_label.UILabel(pygame.Rect((40, 50), (150, 30)),
                                                 text=str(f'Уровень: {Globals.level_count + 1}'),
                                                 manager=manager)

            pygame_gui.elements.ui_label.UILabel(pygame.Rect((40, 100), (150, 30)),
                                                 text=str(f'Рубеж: {Globals.stage_count}'),
                                                 manager=manager)

            pygame_gui.elements.ui_label.UILabel(pygame.Rect((40, 150), (150, 30)),
                                                 text=str(f'Сила атаки: {player.damage}'),
                                                 manager=manager)

        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(Globals.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == begin_btn:
                            Globals.game_cycle = True
                            is_running = False

                        if event.ui_element == exit_btn:
                            is_running = False
                            if Globals.game_cycle:
                                with open('data/character_save.txt', mode='w', encoding='utf8') as file:
                                    file.write(str(player.health) +
                                               '\n' + str(player.damage) +
                                               '\n' + str(player.sphere_defence) +
                                               '\n' + str(Globals.level_count) +
                                               '\n' + str(Globals.stage_count) + '\n')
                                pygame.quit()

                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)

            pygame.display.update()


player = Player((50, 540), 300, 35)
bow = Bow((player.rect.x + 20, player.rect.y + 25, 20, 20), 35)
Menu('Начать игру')

with open('data/character_save.txt', mode='r', encoding='utf8') as file:
    numbers = file.read().split('\n')
    if numbers != ['']:
        player.health = int(numbers[0])
        player.damage = int(numbers[1])
        player.sphere_defence = int(numbers[2])
        Globals.level_count = int(numbers[3])
        Globals.stage_count = int(numbers[4])

HealthBar((300 / (300 / player.health)), 10)
certain = Certain()

# ------------------------------------- Globals.game_cycle ----------------------------------

while Globals.game_cycle:  # Тут идёт загрузка и сохранение карты, а так же его элементов
    Wall((-25, 0))
    Wall((Globals.WIDTH + 1, 0))
    if new_level:
        generate_level()
    else:
        with open('data/map.txt', mode='r', encoding='utf8') as level:
            structure = level.read()
            if structure:
                structure = structure.split('\n')
                Globals.level_base = []
                for y in range(len(structure) - 1):
                    Globals.level_base.append([int(element) for element in structure[y].split(' ')])
                generate(Globals.level_base)
            else:
                generate_level()

    new_level = True
    with open('data/map.txt', mode='w', encoding='utf8') as level:
        result = ''
        for y in range(len(Globals.level_base)):
            row = [str(element) for element in Globals.level_base[y]]
            result += ' '.join([str(element) for element in Globals.level_base[y]]) + '\n'
        level.write(result)
    Globals.level_base = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [2, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [23, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    main_function()
    with open('data/character_save.txt', mode='w', encoding='utf8') as file:
        file.write(str(player.health) + '\n' + str(player.damage) + '\n' + str(player.sphere_defence) + \
                   '\n' + str(Globals.level_count) + '\n' + str(Globals.stage_count) + '\n')

pygame.quit()
