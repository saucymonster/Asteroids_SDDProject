import pygame
import os


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (153, 204, 0)


pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(
    os.path.join('Assets', 'Avatar.png'))
pygame.display.set_icon(icon)

redImg = pygame.image.load(
    os.path.join('Assets', 'Red.png'))

red_amongus = pygame.transform.scale(redImg, (40, 50))

speed = 5


def draw_window(red):
    win.fill(WHITE)
    win.blit(red_amongus, (red.x, red.y))
    pygame.display.update()


def movement(keypresses, red):
    if keypresses[pygame.K_a]:
        red.x -= speed
    if keypresses[pygame.K_d]:
        red.x += speed
    if keypresses[pygame.K_w]:
        red.y -= speed
    if keypresses[pygame.K_s]:
        red.y += speed


def main(): 
    red = pygame.Rect(100, 250, 40, 50)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keypresses = pygame.key.get_pressed()
        movement(keypresses, red)

        draw_window(red)


if __name__ == "__main__":
    main()
    
