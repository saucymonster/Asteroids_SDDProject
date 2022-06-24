import pygame
import os
import random

def clear_cli():
    os.system('cls' if os.name=='nt' else 'clear_cli')

#Difficulty selection via CLI, can be disabled by setting the fixed_difficulty to true

fixed_difficulty = False
difficulty = 0
while True:
    if fixed_difficulty:
        difficulty = 2
        break
    try:
        print("WELCOME TO ASTEROIDS!\nPlease, select the difficulty options as below\n1 - Easy\n2 - Classic")
        difficulty = int(input("3 - Hard\nYour Selection:"))
        if (0 < difficulty <= 3):
            pass
            break
        else:
            raise ValueError
    except ValueError:
        pass
        clear_cli()

#Easy and Hard DIFFICULTY variables
if difficulty == 1:
    max_ammo = 5
    max_player_health = 5
    max_boss_health = 100
    set_regen_rate = 4
    spawn_timer_alien = 7500
    spawn_timer_asteroid = 1350
    score_multiplier = 1
elif difficulty == 3:
    max_ammo = 2
    max_player_health = 3
    max_boss_health = 300
    set_regen_rate = 0
    spawn_timer_alien = 3000
    spawn_timer_asteroid = 550
    score_multiplier = 4
#SET VARIABLE FOR CLASSIC DIFFICULTY
else:
    max_ammo = 3
    max_player_health = 3
    max_boss_health = 200
    set_regen_rate = 7
    spawn_timer_alien = 5000
    spawn_timer_asteroid = 1000
    score_multiplier = 2

# Pre-defines colour values, used later
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 25, 25)
GREEN = (153, 204, 0)
YELLOW = (255, 255, 0)

# Values that will be used later in the code
FPS = 50
level_num = 1
completion_time = None

# Initialises pygame and font module for text
pygame.init()
pygame.font.init()

# Sets up the game window
win_width, win_height = 400, 500
win_center = (win_width // 2, win_height // 2)
win = pygame.display.set_mode((win_width, win_height))

# Sets a caption and icon for the window
pygame.display.set_caption('Asteroids')
icon = pygame.image.load(os.path.join('Assets', 'asteroid.png')).convert_alpha()
pygame.display.set_icon(icon)

# Preload images used for sprites
player_Img = pygame.image.load(os.path.join('Assets', 'rocket.png')).convert_alpha()
asteroid_Img = pygame.image.load(os.path.join('Assets', 'asteroid.png')).convert_alpha()
alien_Img = pygame.image.load(os.path.join('Assets', 'ufo.png')).convert_alpha()
boss_Img = pygame.image.load(os.path.join('Assets', 'alien.png')).convert_alpha()
laser_Img = pygame.image.load(os.path.join('Assets', 'laser.png')).convert_alpha()
enemy_laser_Img = pygame.image.load(os.path.join('Assets', 'enemy_laser.png')).convert_alpha()

# Sets up fonts and pre-renders text where possible
HUD = pygame.font.Font(os.path.join('Assets', 'Symtext.ttf'), 20)
game_over1 = HUD.render('GAME OVER!', False, BLACK)
game_over2 = HUD.render('[ESC] RELAUNCH TO RETRY', False, BLACK)
game_over3 = HUD.render('AGAIN', False, BLACK)

#load the sound effects
shoot_sound = pygame.mixer.Sound(os.path.join('Assets', 'pop.ogg'))
boom_sound = pygame.mixer.Sound(os.path.join('Assets', 'boom.ogg'))
player_hurt_sound = pygame.mixer.Sound(os.path.join('Assets', 'player_hurt.ogg'))
boss_hurt_sound = pygame.mixer.Sound(os.path.join('Assets', 'player_hurt1.ogg')) # Duplicate file due to Pygame volume mixer limitations
hurt_sound = pygame.mixer.Sound(os.path.join('Assets', 'enemy_hurt.ogg'))

bgm = pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'Assets','bgm.ogg'))
pygame.mixer.init()
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)
boss_hurt_sound.set_volume(0.2)

# Class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_Img, (50, 50))  # Setting player dimensions and assigning an image
        self.rect = self.image.get_rect()
        self.rect.center = win_center
        self.vel = 3  # The player's speed
        self.ammo = max_ammo  # Amount of lasers that can be on screen at once
        self.health = max_player_health # Adjusts maximum health at the beginning and regeneration
        self.health_maximum = self.health # For use with the regeneration system
        self.score = 0  # Variable used for tracking score
        self.regeneration_rate = set_regen_rate  # Sets how often player health regenerates in seconds. If the game is too hard,
        # make this value lower to make it easier

    def update(self):
        keypresses = pygame.key.get_pressed()  # Gets a list of all keys pressed in a frame

        # Checks if player is in bounds and user is pressing a movement key
        # If true, the player is moved in the corresponding direction by self.vel, the pre-determined speed value
        if self.rect.left > 0 and keypresses[pygame.K_a]:
            self.rect.x -= self.vel
        if self.rect.right < win_width and keypresses[pygame.K_d]:
            self.rect.x += self.vel
        if self.rect.top > 0 and keypresses[pygame.K_w]:
            self.rect.y -= self.vel
        if self.rect.bottom < win_height and keypresses[pygame.K_s]:
            self.rect.y += self.vel

    # Function called to make the player shoot
    def shoot_laser(self):
        pygame.mixer.Sound.play(shoot_sound) # Plays the shooting sound
        l1 = Laser(*self.rect.midtop)  # Creates a laser with coordinates of the middle of the top side of the player
        lasers.add(l1)  # Adds laser to 'lasers' sprite group
        projectiles.add(l1)  # Adds laser to 'projectiles' sprite group
        all_sprites.add(l1)  # Adds laser to 'all_sprites' sprite group


# Class for asteroids
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

        # Selects a random point in the target square
        self.target = (random.randrange(target_square_left, target_square_right, 5),
                       random.randrange(target_square_top, target_square_bottom, 5))

        if self.rect.x - self.target[0]:  # Tests if the spawn point is directly above or below the target, to prevent 0
            # division error

            # Determines how much to move asteroid in the x and y direction per frame to move it towards the target
            # point, while still maintaining the preset speed
            gradient = (self.target[1] - self.rect.y) / (self.rect.x - self.target[0])

            self.vel_x = (self.vel / (1 + gradient**2)**0.5) if self.rect.x < self.target[0] else - \
                (self.vel / (1 + gradient**2)**0.5)

            self.vel_y = -(self.vel * gradient) / (1 + gradient**2) ** 0.5 if self.rect.x < self.target[0] else \
                ((self.vel * gradient) / (1 + gradient**2)**0.5)

        else:  # Sets the values to avoid zero division error if the target is directly below the spawn point
            self.vel_x = 0
            self.vel_y = self.vel

    def update(self):
        self.rect.x += self.vel_x  # Moves the asteroid right by an amount of pixels determined in __init__
        self.rect.y += self.vel_y  # Moves the asteroid down by an amount of pixels determined in __init__


# Class for aliens: enemies that go across the screen and shoot lasers that can harm the player
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(alien_Img, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn_range = 50, 200  # A range of y-values where aliens can spawn
        self.rect.center = ((random.random() < 0.5) * (win_width-self.rect.width/2), random.randint(*self.spawn_range))
        # Sets the position of the alien to a random point in the range of y-values on the left and right borders
        self.vel = 3 * (self.rect.x - win_center[0])/abs((self.rect.x - win_center[0]))  # Speed value of the alien, is
        # negative if the alien spawns on the right border
        self.frame_count = 0  # Used for timing when lasers get shot
        self.bullet_clock = 0.5  # How often the lasers are shot in seconds

    # Function called to make an alien shoot
    def enemy_laser(self):
        l1 = EnemyLaser(*self.rect.midbottom)
        enemy_lasers.add(l1)
        enemies.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)
        pygame.mixer.Sound.play(shoot_sound)

    # Function to move the alien and shoot every self.bullet_clock seconds
    def update(self):
        self.rect.x -= self.vel
        self.frame_count += 1/clock.get_fps()
        if self.frame_count >= self.bullet_clock:
            self.enemy_laser()
            self.frame_count = 0


# Class for boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(boss_Img, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (win_center[0], 0)
        self.vel = 2
        self.max_health = max_boss_health
        self.health = self.max_health
        self.frame_count = 0
        self.bullet_clock = 0.8
        self.spawning = True  # Is true when the boss is in its spawning phase

    # Function used to move the boss and make it shoot lasers
    def update(self):
        if self.spawning:
            self.rect.y += 1
            if self.rect.bottom == 250:
                self.spawning = False
        # Moves the boss down slowly until it reaches y = 250 if it is in its spawning phase, and sets
        # self.spawning to False

        else:  # If the boss is not in its spawning animation:
            self.rect.x += self.vel  # Moves the boss self.vel pixels to the right
            if self.rect.right >= win_width or self.rect.x <= 0:
                self.vel *= -1  # Makes the boss "bounce" off the borders

            self.frame_count += 1

            if self.health < self.max_health/10:  # If the boss has lost 90% of its health:
                self.bullet_clock = 0.2  # Increases rate of lasers to 0.2 seconds inbetween shots
            elif self.health < self.max_health/2:  # If the boss has lost 50% of its health:
                self.bullet_clock = 0.5  # Increases rate of lasers to 0.5 seconds inbetween shots

            # Shoots a laser every self.bullet_clock seconds
            if self.frame_count/clock.get_fps() >= self.bullet_clock:
                self.shoot_laser()
                self.frame_count = 0

    # Function to make the boss shoot a laser
    def shoot_laser(self):
        l1 = EnemyLaser(random.randint(self.rect.left, self.rect.right-5), self.rect.bottom)
        enemy_lasers.add(l1)
        enemies.add(l1)
        projectiles.add(l1)
        all_sprites.add(l1)


# Class for player-made lasers
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_Img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel = 10

    def update(self):
        self.rect.y -= self.vel  # Moves up laser by self.vel pixels


# Class for enemy-made lasers
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_laser_Img
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel = 10

    def update(self):
        self.rect.y += self.vel  # Moves down laser by self.vel pixels


ship = Player()  # Player object

# Sprite groups
enemies = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
aliens = pygame.sprite.Group()
the_boss = pygame.sprite.GroupSingle()
projectiles = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
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

# Function to handle events that happen every level
def handle_events():
    global level_num
    for event in pygame.event.get():
        if event.type == spawn_asteroid:  # If the spawn_asteroid event occurs:
            # Creates an asteroid object and adds it to the corresponding groups
            A1 = Asteroid()
            asteroids.add(A1)
            projectiles.add(A1)
            enemies.add(A1)
            all_sprites.add(A1)

        if event.type == spawn_alien:  # If a spawn_alien event occurs:
            # Creates an asteroid object and adds it to the corresponding groups
            A1 = Alien()
            aliens.add(A1)
            projectiles.add(A1)
            enemies.add(A1)
            all_sprites.add(A1)

        # If the user presses the quit button or the escape button, closes the window and ends the program
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        # Shoots a laser from the player when the user presses space
        # Plays the shooting sound
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(lasers) < ship.ammo:
                ship.shoot_laser()

        if event.type == regenerate:
            ship.health += 1 if ship.health < ship.health_maximum else 0
        # If a regenerate event happens, adds 1 to the player's health if it is below the maximum

        if event.type == next_lvl:
            level_num += 1
        # If a next_lvl event happens, adds 1 to the variable that tracks the level (i.e. advances to the next level)

        if event.type == spawn_boss:
            boss = Boss()
            the_boss.add(boss)
            all_sprites.add(boss)
        # If a spawn_boss event happens, creates a boss object and adds it to the corresponding groups


# Function find colliding sprites and do the appropriate action
def handle_collisions():
    global level_num
    for projectile in projectiles:
        if not pygame.Rect(0, 0, win_width, win_height).colliderect(projectile.rect):
            projectile.kill()  # .kill() removes the sprite it is called on from all groups, including all_sprites
    # Test every projectile to see if they are off-screen, then kill it

    if pygame.sprite.spritecollide(ship, enemies, True):
        ship.health -= 1
        pygame.mixer.Sound.play(player_hurt_sound)
    # If the player collides with an enemy (which includes enemy-made lasers), subtract 1 health from the player,
    # and kill the enemy
    # Plays the damage sound

    if pygame.sprite.spritecollideany(ship, the_boss):
        ship.rect.y += 10
        ship.health -= 1
        pygame.mixer.Sound.play(player_hurt_sound)
    # If the player collides with the boss, then move the player down 10 pixels and subtract 1 health from the player
    # Plays the damage sound

    if not ship.health:
        death()
    # If the player has no health, call the death function

    if pygame.sprite.groupcollide(lasers, asteroids, True, True):
        ship.score += 50 * score_multiplier
        pygame.mixer.Sound.play(boom_sound)
    # If a player-made laser collides with an asteroid, kill both entities and add 100 score.
    # Also plays an explosion sound

    if pygame.sprite.groupcollide(lasers, aliens, True, True):
        ship.score += 150 * score_multiplier
        pygame.mixer.Sound.play(hurt_sound)
    # If a player-made laser collides with an alien, kill both entities and add 300 score.
    # Also plays a different explosion sound

    if pygame.sprite.groupcollide(lasers, the_boss, True, False):  # If a player made laser collides with the boss, then
        for boss in the_boss:
            boss.health -= 1 if not boss.spawning else 0  # Only removes boss health by one while not in spawning phase
            pygame.mixer.Sound.play(boss_hurt_sound) # Quieter variant of the player hurt sound

            if boss.health == 0:  # If the boss' health is zero, then:
                boss.kill()  # Kill the boss
                pygame.mixer.Sound.play(hurt_sound) # BOOM sound
                ship.score += 5000 * score_multiplier # Add =10,000 score
                level_num += 1  # Go to the next level


# Function for drawing and updating sprites and text onto the game window every frame
def redraw_game_window():
    global completion_time
    win.fill(BLACK)  # Make the whole game window black. This is done first so sprites and text can be drawn on top

    all_sprites.update()  # Call the update function on every sprite in all_sprites
    all_sprites.draw(win)  # Blit every sprite in all_sprites onto the screen at the coordinates specified in the object

    win.blit(HUD.render(f'HEALTH: {ship.health}', False, WHITE), (10, 0))
    # Render and blit the text indicating the player's health in the top left of the game window

    score_text = HUD.render(f'SCORE: {ship.score}', False, WHITE)  # Render the text indicating the player's score
    score_text_rect = score_text.get_rect()
    score_text_rect.right = win_width - 10
    win.blit(score_text, score_text_rect)  # Blit the text in the top right of the game window

    level_text = HUD.render(f'LEVEL {level_num}', False, WHITE) if level_num < 4\
        else HUD.render(f'THANKS FOR PLAYING', False, WHITE)  # Render the text showing the level that the player is on
    # If level_num is greater than 3, then render text that says a thankyou instead
    level_text_rect = level_text.get_rect()
    level_text_rect.bottomleft = 10, win_height
    win.blit(level_text, level_text_rect)  # Blit the text in the bottom left of the game window

    objective_text = 1  # Pre-assigning objective_text variable to prevent a warning message from PyCharm
    if level_num == 1:
        objective_text = HUD.render(f'SURVIVE {round(30 - pygame.time.get_ticks() / 1000)} SECS', False, WHITE)
        # Render text showing the objective of level 1
    elif level_num == 2:
        objective_text = HUD.render(f'SURVIVE {round(30 - pygame.time.get_ticks() / 1000 + 60)} SECS', False, WHITE)
        # Render text showing the objective of level 2
    elif level_num == 3:
        objective_text = HUD.render(f'DEFEAT THE BOSS', False, WHITE)
        # Render text showing the objective of level 3
    elif level_num > 3:
        objective_text = HUD.render('', False, WHITE)

    objective_text_rect = objective_text.get_rect()
    objective_text_rect.bottomright = win_width - 10, win_height
    win.blit(objective_text, objective_text_rect)  # Blit the objective text in the bottom right of the game window

    for boss in the_boss:
        if not boss.spawning:  # If the boss is not in its spawning phase, then:

            # Draw a boss bar
            boss_bar = pygame.Rect(0, 0, 200, 30)
            boss_bar.center = (win_center[0], 50)
            pygame.draw.rect(win, WHITE, boss_bar, 5)
            pygame.draw.rect(win, RED, (105, 40, (boss.health/boss.max_health)*190, 20))

    if level_num > 3:  # If the level is more than 3, then:
        if not completion_time: completion_time = round(pygame.time.get_ticks() / 1000)
        win.blit(HUD.render(f'COMPLETION TIME: {completion_time} SECONDS', False, WHITE), (10, 100))  # Blit and
        # render text showing how fast the game was beaten
        win.blit(HUD.render(f'FINAL SCORE: {ship.score}', False, WHITE), (10, 130))  # Blit and render text showing
        # the final score obtained

    pygame.display.update()  # Update the game window


# Function used when the player dies
def death():
    #Stops Music and sounds
    pygame.mixer.music.fadeout(1000)

    # Kill all entities
    for entity in all_sprites:
        entity.kill()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            # Closes the window and ends the program if the player presses quit or the escape button
        win.fill(RED)  # Fills the window with the colour red

        # Blits pre-rendered death text on the window, and tells the user their final score and how to try again
        win.blit(game_over1, (30, 100))
        win.blit(game_over2, (30, 150))
        #win.blit(game_over3, (30, 180))
        pygame.display.update()

if not ship.regeneration_rate == 0: #Disables regenerate if set to 0
    pygame.time.set_timer(regenerate, ship.regeneration_rate * 1000)  # Sets a regenerate event to occur on a clock

pygame.time.set_timer(spawn_asteroid, spawn_timer_asteroid)  # Sets a spawn_asteroid event to occur every second
pygame.time.set_timer(next_lvl, 30000, 1)  # Sets a next_lvl event to occur in 30 seconds

# Level 1 loop
while level_num == 1:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

pygame.time.set_timer(spawn_alien, spawn_timer_alien)  # Sets a spawn_alien event to occur every 5 seconds
pygame.time.set_timer(next_lvl, 60000, 1)  # Sets a next_lvl event to occur in a minute

# Level 2 loop
while level_num == 2:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

pygame.time.set_timer(spawn_alien, 0)  # Disables the spawn_alien event timer
pygame.time.set_timer(spawn_asteroid, 0)  # Disables the spawn_alien event timer
pygame.time.set_timer(spawn_boss, 3000, 1)  # Sets a spawn_boss event to occur in 3 seconds, once

# Level 3 loop
while level_num == 3:
    clock.tick(FPS)
    handle_events()
    handle_collisions()
    redraw_game_window()

# End screen loop
while True:
    clock.tick(FPS)
    handle_events()
    redraw_game_window()
