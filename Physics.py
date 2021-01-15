import pygame
from Globals import Globals


def gravity_work(character):
    try:
        assert character.jumping
        try:
            assert character.speed_y > -character.max_speed_y
            character.speed_y += -Globals.GRAVITY
        except AssertionError:
            character.falling = True
            character.jumping = False
    except AssertionError:
        try:
            assert character.falling
            try:
                assert character.speed_y < character.max_speed_y
                character.speed_y += Globals.GRAVITY
            except AssertionError:
                pass
        except AssertionError:
            pass


def collision_work(character):
    standing = False
    for tile in Globals.tiles:
        try:
            assert pygame.sprite.collide_rect(character, tile)
            try:
                assert character.max_speed_x >= character.rect.left - tile.rect.right >= \
                       -character.max_speed_x and character.speed_x < 0
                character.rect.left = tile.rect.right
                try:
                    assert character.have_ricochet
                    character.speed_x = -character.speed_x
                except AttributeError:
                    character.speed_x = 0
            except AssertionError:
                pass

            try:
                assert character.max_speed_x >= character.rect.right - tile.rect.left >= \
                       -character.max_speed_x and character.speed_x > 0
                character.rect.right = tile.rect.left
                try:
                    assert character.have_ricochet
                    character.speed_x = -character.speed_x
                except AttributeError:
                    character.speed_x = 0
            except AssertionError:
                pass

            try:
                assert character.max_speed_y >= character.rect.bottom - tile.rect.top >= \
                       -character.max_speed_y and character.speed_y > 0
                character.rect.bottom = tile.rect.top
                try:
                    assert character.have_ricochet
                    character.speed_y = -character.speed_y
                except AttributeError:
                    character.speed_y = 0
                    character.falling = False
                    standing = True
            except AssertionError:
                pass

            try:
                assert character.max_speed_y >= character.rect.top - tile.rect.bottom >= \
                       -character.max_speed_y and character.speed_y < 0
                character.rect.top = tile.rect.bottom
                try:
                    assert character.have_ricochet
                    character.speed_y = -character.speed_y
                except AttributeError:
                    character.speed_y = 0
                    character.falling = True
                    character.jumping = False
            except AssertionError:
                pass
        except AssertionError:
            pass
        try:
            assert character.rect.bottom == tile.rect.top and not standing
            character.falling = True
        except AssertionError:
            pass


def bullet_physics(player):
    for bullet in Globals.player_bullets:
        for enemy in Globals.enemies_hit_boxes:
            if pygame.sprite.collide_mask(bullet, enemy):
                enemy.health -= player.damage
                Globals.player_bullets.remove(bullet)
                Globals.all_sprites.remove(bullet)
                if enemy.health <= 0:
                    Globals.all_sprites.remove(enemy)
                    Globals.enemies.remove(enemy)
                    Globals.enemies_hit_boxes.pop(Globals.enemies_hit_boxes.index(enemy))

        if pygame.sprite.spritecollideany(bullet, Globals.tiles):
            Globals.player_bullets.remove(bullet)
            Globals.all_sprites.remove(bullet)

    for bullet in Globals.enemy_bullets:
        if pygame.sprite.spritecollideany(bullet, Globals.tiles):
            Globals.all_sprites.remove(bullet)
            Globals.enemy_bullets.remove(bullet)
