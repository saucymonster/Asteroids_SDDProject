import pygame
import os


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (153, 204, 0)
grav = 0.5

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption('HUGe man')
icon = pygame.image.load(
    os.path.join('Assets', 'Avatar.png'))
pygame.display.set_icon(icon)

red_image = pygame.image.load(
    os.path.join('Assets', 'Red.png'))


class Player:
    def __init__(self, x, y, width, height, image):
        self.box = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.vel = 3
        self.isJump = False
        self.jump_vel = -15

    def draw(self, hit_box=False):
        win.blit(self.image, (self.box.x, self.box.y))
        if hit_box:
            pygame.draw.rect(win, GREEN, (self.box.x, self.box.y, self.box.width, self.box.height), 1)

    def move(self, keypresses):
        if keypresses[pygame.K_LEFT] and self.box.x > 0:
            self.box.x -= self.vel
        if keypresses[pygame.K_RIGHT] and self.box.right < 500:
            self.box.x += self.vel
        if keypresses[pygame.K_SPACE] and not self.isJump:
            self.isJump = 1

        if self.isJump:
            if self.box.bottom + self.jump_vel < 500:
                self.box.y += self.jump_vel
                self.jump_vel += grav
            else:
                self.isJump = 0
                self.jump_vel = -15
                self.box.bottom = 500


def draw_window(red):
    win.fill(WHITE)
    red.draw(True)
    pygame.display.update()


def main(): 
    red = Player(100, 250, 40, 50, red_image)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(50)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

        keypresses = pygame.key.get_pressed()
        red.move(keypresses)

        draw_window(red)


if __name__ == "__main__":
    main()
