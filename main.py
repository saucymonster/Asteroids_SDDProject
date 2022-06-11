import pygame
import os
import random
import time


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
grav = 0.5

pygame.init()
pygame.font.init()

win_width, win_height = 500, 500
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(
    os.path.join('Assets', 'Avatar.png'))
pygame.display.set_icon(icon)

player_Img = pygame.image.load(os.path.join('Assets', 'Red.png'))
asteroid_Img = pygame.image.load(os.path.join('Assets', 'asteroid.png'))

sans = pygame.font.SysFont('Comic Sans MS', 30)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_Img, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (win_width/2, win_height/2)
        self.vel = 3

    def move(self):
        keypresses = pygame.key.get_pressed()

        if self.rect.left > 0 and keypresses[pygame.K_a]:
            self.rect.x -= self.vel
        if self.rect.right < win_width and keypresses[pygame.K_d]:
            self.rect.x += self.vel
        if self.rect.top > 0 and keypresses[pygame.K_w]:
            self.rect.y -= self.vel
        if self.rect.bottom < win_height and keypresses[pygame.K_s]:
            self.rect.y += self.vel

    def draw(self, hit_rect=False):
        win.blit(self.image, self.rect)
        if hit_rect:
            pygame.draw.rect(win, GREEN, self.rect, 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(asteroid_Img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (30, 30)
        self.vel = 10

    def move(self):
        self.rect.y += self.vel
        if self.rect.bottom >= win_height:
            self.rect.y = 0
            self.rect.x = random.randint(0, 490)

    def draw(self, hit_rect=False):
        win.blit(self.image, self.rect)
        if hit_rect:
            pygame.draw.rect(win, GREEN, self.rect, 1)


red = Player()
A1 = Asteroid()

# Sprite groups
asteroids = pygame.sprite.Group()
asteroids.add(A1)
all_sprites = pygame.sprite.Group()
all_sprites.add(red)
all_sprites.add(A1)

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
    win.fill(WHITE)

    for entity in all_sprites:
        entity.draw(True)
        entity.move()

    if pygame.sprite.spritecollideany(red, asteroids):
        win.fill(RED)
        win.blit(sans.render('dumbass you died to one guy', False, BLACK), (0, win_height / 2))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        SystemExit

    pygame.display.update()
