import pygame
import os
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
YELLOW = (255, 255, 0)
FPS = 50
level_num = 1
completion_time = None

pygame.init()
pygame.font.init()

win_width, win_height = 400, 500
win_center = (win_width // 2, win_height // 2)
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('Asteroids')
icon = pygame.image.load(os.path.join('Assets', 'asteroid.png')).convert_alpha()
pygame.display.set_icon(icon)

player_Img = pygame.image.load(os.path.join('Assets', 'rocket.png')).convert_alpha()
asteroid_Img = pygame.image.load(os.path.join('Assets', 'asteroid.png')).convert_alpha()
alien_Img = pygame.image.load(os.path.join('Assets', 'ufo.png')).convert_alpha()
boss_Img = pygame.image.load(os.path.join('Assets', 'alien.png')).convert_alpha()
laser_Img = pygame.image.load(os.path.join('Assets', 'laser.png')).convert_alpha()
enemy_laser_Img = pygame.image.load(os.path.join('Assets', 'enemy_laser.png')).convert_alpha()


HUD = pygame.font.Font(os.path.join('Assets', 'Symtext.ttf'), 20)
story = pygame.font.Font(os.path.join('Assets', 'Symtext.ttf'), 40)
game_over1 = HUD.render('YOU DIED!', False, BLACK)
game_over2 = HUD.render('QUIT AND RELAUNCH TO TRY', False, BLACK)
game_over3 = HUD.render('AGAIN', False, BLACK)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_Img, (50, 50))
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

        if self.rect.x - self.target[0]:  # To prevent 0 division error

            # Determines how much to move asteroid in the x and y direction per frame to move it towards the target
            # point, while still maintaining the preset speed
            gradient = (self.target[1] - self.rect.y) / (self.rect.x - self.target[0])

            self.vel_x = (self.vel / (1 + gradient**2)**0.5) if self.rect.x < self.target[0] else - \
                (self.vel / (1 + gradient**2)**0.5)

            self.vel_y = -(self.vel * gradient) / (1 + gradient**2) ** 0.5 if self.rect.x < self.target[0] else \
                ((self.vel * gradient) / (1 + gradient**2)**0.5)

        else:  # If the target is directly below the spawn point, then set the values to avoid zero division error
            self.vel_x = 0
            self.vel_y = self.vel

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(alien_Img, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn_range = 50, 200
        self.rect.center = ((random.random() < 0.5) * (win_width-self.rect.width/2), random.randint(*self.spawn_range))
        self.vel = 3 * (self.rect.x - win_center[0])/abs((self.rect.x - win_center[0]))
        self.frame_count = 0
        self.bullet_clock = 0.5

    def enemy_laser(self):
        l1 = EnemyLaser(*self.rect.midbottom)
        enemy_lasers.add(l1)
        enemies.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)

    def update(self):
        self.rect.x -= self.vel
        self.frame_count += 1/clock.get_fps()
        if self.frame_count >= self.bullet_clock:
            self.enemy_laser()
            self.frame_count = 0


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(boss_Img, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (win_center[0], 0)
        self.vel = 2
        self.max_health = 200
        self.health = self.max_health
        self.frame_count = 0
        self.bullet_clock = 0.8
        self.spawning = True

    def update(self):
        if self.spawning:
            self.rect.y += 1
            if self.rect.bottom == 250:
                self.spawning = False
        else:
            self.rect.x += self.vel
            if self.rect.right >= win_width or self.rect.x <= 0:
                self.vel *= -1
            self.frame_count += 1

            if self.health < self.max_health/10:
                self.bullet_clock = 0.2
            elif self.health < self.max_health/2:
                self.bullet_clock = 0.5

            if self.frame_count/clock.get_fps() >= self.bullet_clock:
                self.shoot_laser()
                self.frame_count = 0

    def shoot_laser(self):
        l1 = EnemyLaser(random.randint(self.rect.left, self.rect.right-5), self.rect.bottom)
        enemy_lasers.add(l1)
        enemies.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_Img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel = 10

    def update(self):
        self.rect.y -= self.vel


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_laser_Img
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
the_boss = pygame.sprite.GroupSingle()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(ship)

# Events
next_lvl = pygame.USEREVENT
regenerate = pygame.USEREVENT + 1
spawn_asteroid = pygame.USEREVENT + 2
spawn_alien = pygame.USEREVENT + 3
spawn_boss = pygame.USEREVENT + 4

# Clock object to keep FPS constant
clock = pygame.time.Clock()


def handle_events():
    global level_num
    for event in pygame.event.get():
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

        if event.type == spawn_boss:
            boss = Boss()
            the_boss.add(boss)
            all_sprites.add(boss)


def handle_collisions():
    global level_num
    for projectile in projectiles:
        if not pygame.Rect(0, 0, win_width, win_height).colliderect(projectile.rect):
            projectile.kill()

    if pygame.sprite.spritecollide(ship, enemies, True):
        ship.health -= 1
        if not ship.health:
            death()

    if pygame.sprite.spritecollideany(ship, the_boss):
        ship.rect.y += 10
        ship.health -= 1
        if not ship.health:
            death()

    if pygame.sprite.groupcollide(lasers, asteroids, True, True):
        ship.score += 100

    if pygame.sprite.groupcollide(lasers, the_boss, True, False):
        for boss in the_boss:

            boss.health -= 1 if not boss.spawning else 0

            if boss.health == 0:
                boss.kill()
                ship.score += 10000
                level_num += 1

    if pygame.sprite.groupcollide(lasers, aliens, True, True):
        ship.score += 300


def redraw_game_window():
    global completion_time
    win.fill(BLACK)

    all_sprites.update()
    all_sprites.draw(win)

    win.blit(HUD.render(f'HEALTH: {ship.health}', False, WHITE), (10, 0))

    score_text = HUD.render(f'SCORE: {ship.score}', False, WHITE)
    score_text_rect = score_text.get_rect()
    score_text_rect.right = win_width - 10
    win.blit(score_text, score_text_rect)

    level_text = HUD.render(f'LEVEL {level_num}', False, WHITE) if level_num < 4\
        else HUD.render(f'THANKS FOR PLAYING', False, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.bottomleft = 10, win_height
    win.blit(level_text, level_text_rect)

    objective_text = 1
    if level_num == 1:
        objective_text = HUD.render(f'SURVIVE {round(61 - pygame.time.get_ticks() / 1000)} SECS', False, WHITE)
    elif level_num == 2:
        objective_text = HUD.render(f'SURVIVE {round(61 - pygame.time.get_ticks() / 1000) + 60} SECS', False, WHITE)
    elif level_num == 3:
        objective_text = HUD.render(f'DEFEAT THE BOSS', False, WHITE)
    elif level_num > 3:
        objective_text = HUD.render('', False, WHITE)

    for boss in the_boss:
        if not boss.spawning:
            boss_bar = pygame.Rect(0, 0, 200, 30)
            boss_bar.center = (win_center[0], 50)
            pygame.draw.rect(win, WHITE, boss_bar, 5)
            pygame.draw.rect(win, RED, (105, 40, (boss.health/boss.max_health)*190, 20))

    objective_text_rect = objective_text.get_rect()
    objective_text_rect.bottomright = win_width - 10, win_height
    win.blit(objective_text, objective_text_rect)

    if level_num > 3:
        if not completion_time: completion_time = round(pygame.time.get_ticks() / 1000)
        win.blit(HUD.render(f'COMPLETION TIME: {completion_time} SECONDS', False, WHITE), (10, 100))
        win.blit(HUD.render(f'FINAL SCORE: {ship.score}', False, WHITE), (10, 130))

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
        win.blit(game_over1, (30, 100))
        win.blit(game_over2, (30, 150))
        win.blit(game_over3, (30, 180))
        pygame.display.update()


pygame.time.set_timer(regenerate, 10000)
pygame.time.set_timer(spawn_asteroid, 1000)
pygame.time.set_timer(next_lvl, 60000, 2)
while level_num == 1:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

pygame.time.set_timer(spawn_alien, 5000)
while level_num == 2:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

pygame.time.set_timer(spawn_alien, 0)
pygame.time.set_timer(spawn_asteroid, 0)
pygame.time.set_timer(spawn_boss, 1, 1)
while level_num == 3:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

while True:
    clock.tick(FPS)
    handle_events()
    redraw_game_window()
