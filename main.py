import pygame
import os
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
YELLOW = (255, 255, 0)
debug = False
FPS = 50
level_num = 2

pygame.init()
pygame.font.init()

win_width, win_height = 400, 500
win_center = (win_width // 2, win_height // 2)
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(os.path.join('Assets', 'Avatar.png')).convert_alpha()
pygame.display.set_icon(icon)

player_Img = pygame.image.load(os.path.join('Assets', 'Red.png')).convert_alpha()
asteroid_Img = pygame.image.load(os.path.join('Assets', 'asteroid.png')).convert_alpha()
alien_Img = pygame.image.load(os.path.join('Assets', 'ufo.png')).convert_alpha()
laser_Img = pygame.image.load(os.path.join('Assets', 'laser.png')).convert_alpha()
enemy_laser_Img = pygame.image.load(os.path.join('Assets', 'enemy_laser.png')).convert_alpha()

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

    def update(self):
        keypresses = pygame.key.get_pressed()

        if self.rect.left > 0 and keypresses[pygame.K_a]:
            self.rect.x -= self.vel
        if self.rect.right < win_width and keypresses[pygame.K_d]:
            self.rect.x += self.vel
        if self.rect.top > 0 and keypresses[pygame.K_w]:
            self.rect.y -= self.vel
        if self.rect.bottom < win_height and keypresses[pygame.K_s]:
            self.rect.y += self.vel

    def shoot_laser(self):
        l1 = Laser(*self.rect.midtop)
        lasers.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)

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

            self.vel_x = (self.vel / (1 + gradient**2)**0.5) if self.rect.x < self.target[0] else - \
                (self.vel / (1 + gradient**2)**0.5)

            self.vel_y = -(self.vel * gradient) / (1 + gradient**2) ** 0.5 if self.rect.x < self.target[0] else \
                ((self.vel * gradient) / (1 + gradient**2)**0.5)

            if debug: print('m: ', gradient)

        else:  # If the target is directly below the spawn point, then set the values to avoid zero division error
            self.vel_x = 0
            self.vel_y = self.vel

        if debug: print('components: ', self.vel_x, self.vel_y)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self):
        win.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(win, GREEN, self.rect, 1)
            pygame.draw.line(win, WHITE, (self.spawn_x, self.spawn_y), self.target)


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(alien_Img, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn_range = 50, 200
        self.rect.center = ((random.random() < 0.5) * (win_width-self.rect.width/2), random.randint(*self.spawn_range))
        self.vel = 3 * (self.rect.x - win_center[0])/abs((self.rect.x - win_center[0]))
        self.timer = 0
        self.bullet_clock = 0.5

    def enemy_laser(self):
        l1 = EnemyLaser(*self.rect.midbottom)
        enemy_lasers.add(l1)
        enemies.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)

    def update(self):
        self.rect.x -= self.vel
        self.timer += 1/clock.get_fps()
        if self.timer >= self.bullet_clock:
            self.enemy_laser()
            self.timer = 0


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(laser_Img, (5, 10))
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel = 10

    def update(self):
        self.rect.y -= self.vel


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(enemy_laser_Img, (5, 10))
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel = 10

    def update(self):
        self.rect.y += self.vel


ship = Player()

# Sprite groups
asteroids = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
aliens = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(ship)

# Events
next_lvl = pygame.USEREVENT
regenerate = pygame.USEREVENT + 1
spawn_asteroid = pygame.USEREVENT + 2
spawn_alien = pygame.USEREVENT + 3

clock = pygame.time.Clock()


def handle_regular_events(event):
    global level_num
    if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(lasers) < ship.ammo:
            ship.shoot_laser()
    if event.type == regenerate:
        ship.health += 1 if ship.health < 3 else 0
    if event.type == next_lvl:
        level_num += 1


def redraw_game_window():
    win.fill(BLACK)

    all_sprites.update()
    all_sprites.draw(win)

    for projectile in projectiles:
        if not pygame.Rect(0, 0, win_width, win_height).colliderect(projectile.rect):
            projectile.kill()

    if pygame.sprite.spritecollide(ship, enemies, True):
        ship.health -= 1
        if not ship.health:
            death()

    if pygame.sprite.groupcollide(lasers, asteroids, True, True):
        ship.score += 100

    if pygame.sprite.groupcollide(lasers, aliens, True, True):
        ship.score += 300

    win.blit(HUD.render(f'HEALTH: {ship.health}', False, WHITE), (10, 0))

    score_text = HUD.render(f'SCORE: {ship.score}', False, WHITE)
    score_text_rect = score_text.get_rect()
    score_text_rect.right = win_width - 10
    win.blit(score_text, score_text_rect)

    level_text = HUD.render(f'LEVEL {level_num}', False, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.bottomleft = 10, win_height
    win.blit(level_text, level_text_rect)

    objective_text = 1
    if level_num == 1:
        objective_text = HUD.render(f'SURVIVE {round(61 - pygame.time.get_ticks() / 1000)} SECS', False, WHITE)
    elif level_num == 2:
        objective_text = HUD.render(f'SURVIVE {round(61 - pygame.time.get_ticks() / 1000) + 60} SECS', False, WHITE)

    objective_text_rect = objective_text.get_rect()
    objective_text_rect.bottomright = win_width - 10, win_height
    win.blit(objective_text, objective_text_rect)

    pygame.display.update()


def death():
    for entity1 in all_sprites:
        entity1.kill()

    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT or \
                    (event1.type == pygame.KEYDOWN and event1.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
        win.fill(RED)
        win.blit(game_over, (0, win_center[1]))
        pygame.display.update()


pygame.time.set_timer(regenerate, 10000)
pygame.time.set_timer(spawn_asteroid, 1000)
pygame.time.set_timer(next_lvl, 60000, 1)
while level_num == 1:
    clock.tick(FPS)
    for event in pygame.event.get():
        handle_regular_events(event)
        if event.type == spawn_asteroid:
            A1 = Asteroid()
            asteroids.add(A1)
            projectiles.add(A1)
            all_sprites.add(A1)
            enemies.add(A1)

    redraw_game_window()

pygame.time.set_timer(spawn_alien, 5000)
while level_num == 2:
    clock.tick(FPS)
    for event in pygame.event.get():
        handle_regular_events(event)
        if event.type == spawn_asteroid:
            A1 = Asteroid()
            asteroids.add(A1)
            projectiles.add(A1)
            enemies.add(A1)
            all_sprites.add(A1)

        if event.type == spawn_alien:
            A1 = Alien()
            aliens.add(A1)
            projectiles.add(A1)
            enemies.add(A1)
            all_sprites.add(A1)

    redraw_game_window()
