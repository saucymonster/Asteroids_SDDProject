import pygame
import os
import random
import time
import math


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
grav = 0.5

pygame.init()
pygame.font.init()

win_width, win_height = 500, 500
win_center = (win_width//2, win_height//2)
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
        self.rect.center = win_center
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

    def draw(self, hit_box=False):
        win.blit(self.image, self.rect)
        if hit_box:
            pygame.draw.rect(win, GREEN, self.rect, 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(asteroid_Img, (20, 20))
        self.rect = self.image.get_rect()
        self.vel = 10
        self.vel_x, self.vel_y = math.sqrt(self.vel), math.sqrt(self.vel)
        self.border_right, self.border_bottom = win_width - self.rect.width, win_height - self.rect.height
        self.rect.x, self.rect.y = -100, -100
        self.spawn_x, self.spawn_y, self.target = 0, 0, (0, 0)

    def spawn(self):
        if random.random() < 0.5:  # Coinflip to decide which pair of sides (horizontal or vertical) the asteroid
            # should spawn on
            self.spawn_x = (random.random() < 0.5) * self.border_right  # Determines one side from the pair
            self.spawn_y = random.randint(0, self.border_bottom)  # Asteroid can spawn anywhere on that side
        else:
            self.spawn_x = random.randint(0, self.border_right)
            self.spawn_y = (random.random() < 0.5) * self.border_bottom

        return self.spawn_x, self.spawn_y

    def move(self):
        if not pygame.Rect(0, 0, win_width, win_height).colliderect(self.rect):  # If the asteroid is off-screen, then:
            self.spawn()
            self.rect.x, self.rect.y = self.spawn_x, self.spawn_y

            # Defining target square and boundaries
            target_square_len = 100
            target_square_right = win_center[0] + target_square_len//2
            target_square_left = win_center[0] - target_square_len//2
            target_square_bottom = win_center[1] + target_square_len//2
            target_square_top = win_center[1] - target_square_len//2

            # Select a random point in the target square
            self.target = (random.randrange(target_square_left, target_square_right, 5),
                           random.randrange(target_square_top, target_square_bottom, 5))

            gradient = (self.target[1]-self.spawn_y)/(self.spawn_x - self.target[0])

            self.vel_x = (self.vel/math.sqrt(1+gradient**2)) if self.spawn_x < self.target[0] else -\
                (self.vel/math.sqrt(1+gradient**2))

            self.vel_y = -(self.vel * gradient)/math.sqrt(1+gradient**2) if self.spawn_x < self.target[0] else \
                ((self.vel * gradient)/math.sqrt(1+gradient**2))

            print('\n', self.spawn_x, self.spawn_y)
            print(self.target)
            print(gradient)
            print(self.vel_x, self.vel_y)
        pygame.draw.line(win, BLACK, (self.spawn_x, self.spawn_y), self.target)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, hit_box=False):
        win.blit(self.image, self.rect)
        if hit_box:
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
    clock.tick(20)

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
        win.blit(sans.render('stupid you died to one guy', False, BLACK), (0, win_center[1]))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        exit()

    pygame.display.update()
