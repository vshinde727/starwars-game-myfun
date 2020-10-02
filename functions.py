import pygame
import math
from pygame import mixer

def show_score(x, y, screen, font, curr_score, total_attacks):
    score = font.render("Score : " + str(curr_score) + " ( Bullets left :" + str(total_attacks) + ")", True,
                        (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y, screen, playerImg):
    screen.blit(playerImg, (x, y))


def enemy(x, y, ei, screen, enemyImg):
    screen.blit(enemyImg[ei], (x, y))


def fire_bullet(x, y, screen, bulletImg):
    # global bullet_state
    # bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    return "fire"


def is_collision(enemyX1, enemyY1, bulletX1, bulletY1):
    distance = math.sqrt(math.pow(enemyX1 - bulletX1, 2) + math.pow(enemyY1 - bulletY1, 2))
    return distance < 27


def game_over(msg, rgb, screen, screenSize):
    game_over_font = pygame.font.Font('freesansbold.ttf', 32)
    game_over_text = game_over_font.render(msg, True, rgb)
    game_over_text_rect = game_over_text.get_rect(center=(screenSize['width'] / 2, screenSize['height'] / 2))
    screen.blit(game_over_text, game_over_text_rect)
    if rgb == (255, 0, 0):
        game_over_sound = mixer.Sound('music/goodbye.wav')
        game_over_sound.play()


def bottom_question(msg, rgb, screen, screenSize):
    bottom_question_font = pygame.font.Font('freesansbold.ttf', 32)
    bottom_question_text = bottom_question_font.render(msg, True, rgb)
    bottom_question_text_rect = bottom_question_text.get_rect(
        center=(screenSize['width'] / 2, screenSize['height'] - 40))
    screen.blit(bottom_question_text, bottom_question_text_rect)

def make_video(screen):
    _image_num = 0
    while True:
        _image_num += 1
        str_num = "000" + str(_image_num)
        file_name = "image" + str_num[-4:] + ".jpg"
        pygame.image.save(screen, file_name)
        yield
