import pygame
import os


white = (255,255,255)
red = (255, 0, 0)
green = (153,204,0)


pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(
    os.path.join('Assets', 'Avatar.png'))
pygame.display.set_icon(icon)

redImg = pygame.image.load(
    os.path.join('Assets', 'Red.png'))
orangImg = pygame.image.load(
    os.path.join('Assets','Orange.png'))

red_amongus = pygame.transform.scale(redImg, (40,50))
orang_amongus = pygame.transform.flip(pygame.transform.scale(orangImg, (40,50)), True, False)

speedX = 5

def draw_window(red, orang):
    win.fill(white)
    win.blit(red_amongus, (red.x, red.y))
    win.blit(orang_amongus, (orang.x, orang.y))
    pygame.display.update()



def main(): 
    red = pygame.Rect(100,250,40,50)
    orang = pygame.Rect(400,250,40,50)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keypresses = pygame. 
        

        draw_window(red, orang)


if __name__ == "__main__":
    main()
    
