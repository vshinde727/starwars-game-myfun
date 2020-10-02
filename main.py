# https://www.youtube.com/watch?v=FfWpgLFMI7w
import pygame
import random
import math
from pygame import mixer
from functions import *

# initialize pygame
pygame.init()
difficulty_level = ''
screenSize = {'width': 800, 'height': 600}
difficulty_x = {'pro': -50, 'avg': -30, 'beginner': -20}
difficulty_y = {'pro': 60, 'avg': 50, 'beginner': 40}
num_of_enemies = {'pro': 10, 'avg': 8, 'beginner': 5}
target_scores = {'pro': 20, 'avg': 15, 'beginner': 10}
screen = pygame.display.set_mode((screenSize['width'], screenSize['height']))
closedEvent = False

# Title and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)

# background sound
mixer.music.load('music/star-wars-theme-song.mp3')
mixer.music.play(-1)

# init block - Front screen
stepDownFrontSize = 2
initStep = 1
frontScreen = True
reverse = False
while frontScreen:
    backgroundImg = pygame.image.load('images/Star-Wars-Logo-Art.jpg')  # Should be of same size as that of screen
    if not reverse:
        if ((screenSize['width'] - initStep * stepDownFrontSize) > 300) or (
                (screenSize['height'] - initStep * stepDownFrontSize) > 300):
            initStep = initStep + 3
        else:
            reverse = True
    elif reverse:
        initStep = initStep - 3
        if initStep < 10:
            reverse = False
    backgroundImg = pygame.transform.scale(backgroundImg, (
        screenSize['width'] - initStep * stepDownFrontSize - screenSize['width'] // 20,
        screenSize['height'] - initStep * stepDownFrontSize - screenSize['height'] // 20))
    font = pygame.font.Font('freesansbold.ttf', 24)
    textX = screenSize['width'] // 2
    textY = screenSize['height'] - 40
    screen.blit(backgroundImg, (screenSize['width'] / 10, screenSize['height'] / 10))
    user_input = font.render("Select level to begin star war.. [p - pro, a - avg, b - beginner ]", True, (255, 255, 0))
    user_input_rect = user_input.get_rect(center=(textX, textY))
    screen.blit(user_input, user_input_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            frontScreen = False
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                difficulty_level = 'pro'
                frontScreen = False
            elif event.key == pygame.K_a:
                difficulty_level = 'avg'
                frontScreen = False
            elif event.key == pygame.K_b:
                difficulty_level = 'beginner'
                frontScreen = False
    pygame.display.update()

target_score = target_scores[difficulty_level]
speed = difficulty_y[difficulty_level]

# background images
backgroundImg = pygame.image.load('images/space-bg.jpg')  # Should be of same size as that of screen
backgroundImg = pygame.transform.scale(backgroundImg, (screenSize['width'], screenSize['height']))

# Player
playerImg = pygame.image.load('images/space-invaders.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))

playerX = screenSize['width'] / 2 - 32  # screenSize['width']/2 - 32
playerY = screenSize['height'] - 120
rightLimit = screenSize['width'] - 64
leftLimit = 0
playerX_change = 0

# Enemy
# enemyImg = pygame.images.load('enemy.png')
# enemyX = random.randint(0, screenSize['width'] - 65) # screenSize['width']/2 - 32
# enemyY = random.randint(0, screenSize['height']/12)
# enemyX_change = -5
# enemyY_change = screenSize['height'] /20

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = num_of_enemies[difficulty_level]

for i in range(num_of_enemy):
    enemyImg.append(
        pygame.transform.flip(pygame.transform.scale(pygame.image.load('images/space-invaders-2.png'), (64, 64)), False, True))
    enemyX.append(random.randint(0, screenSize['width'] - 65))
    enemyY.append(random.randint(0, screenSize['height'] // 10))
    enemyX_change.append(difficulty_x[difficulty_level])
    enemyY_change.append(screenSize['height'] / difficulty_y[difficulty_level])

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = random.randint(0, screenSize['width'])  # screenSize['width']/2 - 32
bulletY = screenSize['height'] - 120
bulletX_change = 0
bulletY_change = screenSize['height'] / 10
bullet_state = "ready"

# scoring
total_attacks = 50
curr_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 20


# Functions

running = True
# Need to add quit functionality, otherwise the screen will get hung and wont be able to close
while running:
    # Colour of the screen - 0-255
    screen.fill((0, 0, 0))

    # Set background in each iteration
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closedEvent = True
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            playerX_change = -1 * speed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            playerX_change = speed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if bullet_state == 'ready':
                bullet_sound = mixer.Sound('music/laser.wav')
                bullet_sound.play()
                bulletX = playerX
                total_attacks = total_attacks - 1
                bullet_state = fire_bullet(bulletX, bulletY, screen, bulletImg)
                if total_attacks == 0:
                    for j in range(num_of_enemy):
                        enemyY[j] = 2000
                    game_over("No bullets left, you are defeated in the war", (255, 0, 0), screen, screenSize)
                    running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            playerX_change = 0
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX = playerX + playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= rightLimit:
        playerX = rightLimit

    for i in range(num_of_enemy):
        if enemyY[i] >= playerY - 32:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over('You are defeated in the sky war.. ', (255, 0, 0), screen, screenSize)
            running = False
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 1 * speed
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyX[i] >= rightLimit:
            enemyX_change[i] = -1 * speed
            enemyY[i] = enemyY[i] + enemyY_change[i]
            # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('music/explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            curr_score += 1
            if curr_score >= target_score:
                for j in range(num_of_enemy):
                    enemyY[j] = 2000
                game_over("Congratulations, You won the war!!", (255, 255, 0), screen, screenSize)
                running = False
                break
            enemyX[i] = random.randint(0, screenSize['width'] - 10)  # screenSize['width']/2 - 32
            enemyY[i] = random.randint(0, screenSize['height'] // 8)
        enemy(enemyX[i], enemyY[i], i, screen, enemyImg)

    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = screenSize['height'] - 120
    if bullet_state == 'fire':
        bullet_state = fire_bullet(bulletX, bulletY, screen, bulletImg)
        bulletY = bulletY - bulletY_change

    player(playerX, playerY, screen, playerImg)
    show_score(textX, textY, screen, font, curr_score, total_attacks)
    pygame.display.update()
    if not running and not closedEvent:
        while not running:
            rerun = False
            bottom_question('Press q to quit or r to restart', (255, 255, 0), screen, screenSize)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = True
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        rerun = True
                        running = False
                        break
            if rerun:
                for j in range(num_of_enemy):
                    enemyY[j] = random.randint(0, screenSize['height'] // 8)
                curr_score = 0
                total_attacks = 50
                break
        running = not running



