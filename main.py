import random
import math
import pygame
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('bgd5.jpg')
# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# Title and Window
pygame.display.set_caption("SPACE WARRIORS")
icon = pygame.image.load('space-ship (1).png')
pygame.display.set_icon(icon)
# PLAYER
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change =[]
enemyY_change =[]
num_of_enemies=4
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien (1).png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.6)
    enemyY_change.append(40)
# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_status = 'ready'


# COLLISION
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if (distance < 27):
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_status
    bullet_status = 'Fire'
    screen.blit(bulletImg, (x + 16, y + 10))
#SCORE VALUE
score_value=0
font=pygame.font.Font('DS-DIGII.TTF',32)
textX=10
textY=10
# GAME_OVER TEXT
over_font=pygame.font.Font('DS-DIGII.TTF',80)
def game_over():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(250,250))
def show_score(x,y):
    score=font.render("SCORE:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
# GAME LOOP
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX  # current player position bullet gets
                bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # BOUNDARIES FOR PLAYER
    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:
        playerX = 735
    player(playerX, playerY)
    for i in range(num_of_enemies):
        if enemyY[i] > 380:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over()
                break
        enemyX[i]+= enemyX_change[i]
        # BOUNDARIES FOR ENEMY
        if enemyX[i]<= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>= 735:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]
        Collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if Collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_status = "ready"
            score_value+= 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i],enemyY[i],i)
    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_status = 'ready'
    if bullet_status == 'Fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    show_score(textX,textY)

    pygame.display.update()
