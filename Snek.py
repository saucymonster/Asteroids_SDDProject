#   SNAKE GAME
#   Author : Apaar Gupta (@apaar97)
#   Python 3.5.2 Pygame
#   Original Project Link https://www.pygame.org/project/869

import pygame
import sys
import time
import random
import os

# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
    print("[sudo] missing root privileges\ninitialising errors {0} occurred".format(init_status[1]))
    sys.exit()
else:
    print("[snake@pygame ~]$ pygame.org.snake")
    print("[sudo] missing root privileges")
    time.sleep(1)
    print("[snake@pygame ~]$ sudo pygame.org.snake")
    print("ok")

# Window Icon & Play Surface
#favicon = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/images','snek.png'))
#pygame.display.set_icon(favicon)

size = width, height = 640, 480
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("[snake@pygame ~]$ Snek!.py")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
slate = pygame.Color(30, 30, 30)
white = pygame.Color(255, 255, 255)
red2 = pygame.Color(255, 42, 42)

# FPS controller
fpsController = pygame.time.Clock()

# Game settings (delta breaks detection when changed other than 10)
delta = 10
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [400, 50]
foodSpawn = True
direction = 'RIGHT'
changeto = ''
score = 0


# Game Over
def gameOver():
    myFont = pygame.font.SysFont('comic sans ms', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    print("\n[snake@pygame ~]$ sudo -k")
    pygame.quit()
    sys.exit("\n[snake@pygame ~]$ exit")


# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('comic sans ms', 24)
    Ssurf = SFont.render("{0}".format(score), True, white)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (25, 0)
    else:
        Srect.midtop = (320, 110) 
    playSurface.blit(Ssurf, Srect)

#To Do List : Add buffer system
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validate direction (Preventing Self hit backwards)
    if changeto == 'RIGHT' and direction != 'LEFT':
        direction = changeto
    if changeto == 'LEFT' and direction != 'RIGHT':
        direction = changeto
    if changeto == 'UP' and direction != 'DOWN':
        direction = changeto
    if changeto == 'DOWN' and direction != 'UP':
        direction = changeto

    # Update snake position
    if direction == 'RIGHT':
        snakePos[0] += delta
    if direction == 'LEFT':
        snakePos[0] -= delta
    if direction == 'DOWN':
        snakePos[1] += delta
    if direction == 'UP':
        snakePos[1] -= delta

    # Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos == foodPos:
        foodSpawn = False
        if score <= 999:
           score += 1
    else:
        snakeBody.pop()
    if foodSpawn == False:
        foodPos = [random.randrange(1, width // 10) * delta, random.randrange(1, height // 10) * delta]
        foodSpawn = True

    playSurface.fill(slate)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], delta, delta))
    pygame.draw.rect(playSurface, red2, pygame.Rect(foodPos[0], foodPos[1], delta, delta))

    # Bounds
    if snakePos[0] >= width or snakePos[0] < 0:
        gameOver()
    if snakePos[1] >= height or snakePos[1] < 0:
        gameOver()

    # Self hit
    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()
    showScore()
    pygame.display.flip()
    fpsController.tick(25)
