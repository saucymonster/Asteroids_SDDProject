import pygame
import os
import random
import math
from threading import Timer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
YELLOW = (255, 255, 0)
debug = False
alive = True

pygame.init()
pygame.font.init()

win_width, win_height = 400, 500
win_center = (win_width // 2, win_height // 2)
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(
    os.path.join('Assets', 'Avatar.png'))
pygame.display.set_icon(icon)

player_Img = pygame.image.load(os.path.join('Assets', 'Red.png'))
asteroid_Img = pygame.image.load(os.path.join('Assets', 'asteroid.png'))

sans = pygame.font.SysFont('Comic Sans MS', 30)
HUD = pygame.font.Font(os.path.join('Assets', 'Symtext.ttf'), 20)
game_over = sans.render('stupid u die', False, BLACK)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_Img, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.center = win_center
        self.vel = 3
        self.ammo = 3
        self.health = 3
        self.score = 0

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

    def draw(self):
        win.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(win, GREEN, self.rect, 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(asteroid_Img, (20, 20))
        self.rect = self.image.get_rect()
        self.vel = 7
        self.border_right, self.border_bottom = win_width - self.rect.width, win_height - self.rect.height

        if random.random() < 0.5:  # Coinflip to decide which pair of sides (horizontal or vertical) the asteroid
            # should spawn on
            self.spawn_x = (random.random() < 0.5) * self.border_right  # Determines one side from the pair
            self.spawn_y = random.randint(0, self.border_bottom)  # Asteroid can spawn anywhere on that side
        else:
            self.spawn_x = random.randint(0, self.border_right)
            self.spawn_y = (random.random() < 0.5) * self.border_bottom

        if debug: print('\nspawn pos: ', self.spawn_x, self.spawn_y)
        self.rect.x, self.rect.y = self.spawn_x, self.spawn_y

        # Defining target square and boundaries
        target_square_len = 100
        target_square_right = win_center[0] + target_square_len // 2
        target_square_left = win_center[0] - target_square_len // 2
        target_square_bottom = win_center[1] + target_square_len // 2
        target_square_top = win_center[1] - target_square_len // 2

        # Select a random point in the target square
        self.target = (random.randrange(target_square_left, target_square_right, 5),
                       random.randrange(target_square_top, target_square_bottom, 5))

        if debug: print('target: ', self.target)

        if self.rect.x - self.target[0]:  # To prevent 0 division error
            # Determines how much to move asteroid in the x and y direction per frame to move it towards the target
            # point, while still maintaining the preset speed
            gradient = (self.target[1] - self.rect.y) / (self.rect.x - self.target[0])

            self.vel_x = (self.vel / math.sqrt(1 + gradient**2)) if self.rect.x < self.target[0] else - \
                (self.vel / math.sqrt(1 + gradient**2))

            self.vel_y = -(self.vel * gradient) / math.sqrt(1 + gradient**2) if self.rect.x < self.target[0] else \
                ((self.vel * gradient) / math.sqrt(1 + gradient**2))

            if debug: print('m: ', gradient)

        else:  # If the target is directly below the spawn point, then set the values to avoid zero division error
            self.vel_x = 0
            self.vel_y = self.vel

        if debug: print('components: ', self.vel_x, self.vel_y)

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self):
        win.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(win, GREEN, self.rect, 1)
            pygame.draw.line(win, WHITE, (self.spawn_x, self.spawn_y), self.target)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 5, 10)
        self.rect.center = (x, y)
        self.vel = 10

    def move(self):
        self.rect.y -= self.vel

    def draw(self):
        pygame.draw.rect(win, YELLOW, self.rect)


red = Player()

# Sprite groups
asteroids = pygame.sprite.Group()
lasers = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(red)

spawn_asteroid = pygame.USEREVENT
regenerate = pygame.USEREVENT + 1

pygame.time.set_timer(spawn_asteroid, 2000)
pygame.time.set_timer(regenerate, 10000)

clock = pygame.time.Clock()
while red.health:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                A1 = Asteroid()
                asteroids.add(A1)
                projectiles.add(A1)
                all_sprites.add(A1)
            if event.key == pygame.K_SPACE and len(lasers) < red.ammo:
                L1 = Laser(*red.rect.midtop)
                lasers.add(L1)
                projectiles.add(L1)
                all_sprites.add(L1)
        if event.type == spawn_asteroid:
            A1 = Asteroid()
            asteroids.add(A1)
            projectiles.add(A1)
            all_sprites.add(A1)
        if event.type == regenerate:
            red.health += 1 if red.health < 3 else 0

    win.fill(BLACK)

    for entity in all_sprites:
        entity.draw()
        entity.move()

    for projectile in projectiles:
        if not pygame.Rect(0, 0, win_width, win_height).colliderect(projectile.rect):
            projectile.kill()

    if pygame.sprite.spritecollide(red, asteroids, True):
        red.health -= 1

    win.blit(HUD.render(f'HP: {red.health}', False, WHITE), (10, 0))

    score_rect = HUD.render(f'SCORE: {red.score}', False, WHITE).get_rect()
    score_rect.right = win_width - 10
    win.blit(HUD.render(f'SCORE: {red.score}', False, WHITE), score_rect)
    pygame.display.update()

    if pygame.sprite.groupcollide(lasers, asteroids, True, True):
        red.score += 100


for entity in all_sprites:
    entity.kill()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        win.fill(RED)
        win.blit(game_over, (0, win_center[1]))
        pygame.display.update()
