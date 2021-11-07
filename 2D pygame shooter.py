# Date created: April 24, 2019
# Date last edited: May 6, 2019

import random
import os
import pygame
from pygame import *

# Initializes pygame
pygame.init()

# Shortcut variables
clock = pygame.time.Clock()

# Variables
bullet_counter = 0
win = False
lose = False
side_lasery = 0
side_laserx = 0

# Constants
WIDTH = 1280
HEIGHT = 720
FPS = 60


# Colors (R, G, B)
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
CYAN = 0, 255, 255

# Screen
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centers the window
pygame.display.set_caption('Kill The Blokk!')  # Name of window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Sets window size by using constants and creates window

# Definitions

font_name = pygame.font.match_font('arial')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = x, y
    surface.blit(text_surface, text_rect)


def draw_boss_healthbar(surface, width):

    healthbar_boss = pygame.Rect(0, 0, width, 10)
    pygame.draw.rect(surface, RED, healthbar_boss)




# Classes


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Making sprite
        self.image = pygame.Surface((15, 35))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = x
        self.rect.bottom = y

        # Variables
        self.speedy = -10

    def update(self):
        global bullet_counter  # Uses variable from outside scope
        self.rect.y += self.speedy  # Moves bullet y value
        if self.rect.bottom < 0:
            self.kill()  # Kills bullet if it moves off screen
            bullet_counter -= 1  # Removes a count from the bullet counter whenever a bullet gets killed


class Player(pygame.sprite.Sprite):

    # Code that runs when player is created initially
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)

        # Creating player image and rectangle
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Creating where player spawns
        self.rect.bottom = HEIGHT - 20
        self.rect.centerx = x

        # All the player variables
        self.speedx = 0
        self.speedy = 0
        self.bullet_counter = 0
        self.jump_start = 0
        self.jump_counter = 2

        # All the player booleans
        self.jumping = False
        self.falling = False
        self.standing = True
        self.jump_grace = False
        self.standingOnPlatform = False
        self.fallingThroughPlatformGrace = False
        self.fallingThroughPlatformGraceTimer = 0

    # Code that runs every frame
    def update(self):
        now = pygame.time.get_ticks()  # How long since game has started
        # This code is for movement
        self.speedx = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_LEFT]:
            self.speedx = 0

        # Checking if player falls off platform
        if self.standingOnPlatform:
            if keystate[pygame.K_DOWN]:
                self.jumping = False
                self.falling = True
                self.standing = False
                self.jump_grace = False
                self.standingOnPlatform = False
                self.fallingThroughPlatformGrace = True

            if not pygame.sprite.groupcollide(platform_group, playerG, False, False):
                self.jumping = False
                self.falling = True
                self.standing = False
                self.jump_grace = False
                self.standingOnPlatform = False
                self.fallingThroughPlatformGrace = False

        if self.fallingThroughPlatformGrace:
            self.fallingThroughPlatformGraceTimer = pygame.time.get_ticks()
            if now - self.fallingThroughPlatformGraceTimer > 100:
                self.fallingThroughPlatformGrace = False

        # Player platform control
        if pygame.sprite.groupcollide(platform_group, playerG, False, False):
            if pygame.sprite.spritecollide(platform_right, playerG, False):  # Player colliding with right platform
                if not self.fallingThroughPlatformGrace:
                    if self.rect.bottom <= platform_right.rect.top + 8:
                        if not self.jumping:
                            if not self.jump_grace:
                                self.jumping = False
                                self.falling = False
                                self.standing = False
                                self.jump_grace = False
                                self.standingOnPlatform = True
                                self.fallingThroughPlatformGrace = False
                                self.rect.bottom = platform_right.rect.top + 1
                                self.jump_counter = 2

            if pygame.sprite.spritecollide(platform_left, playerG, False):  # Player colliding with left platform
                if not self.fallingThroughPlatformGrace:
                    if self.rect.bottom <= platform_left.rect.top + 8:
                        if not self.jumping:
                            if not self.jump_grace:
                                self.jumping = False
                                self.falling = False
                                self.standing = False
                                self.jump_grace = False
                                self.standingOnPlatform = True
                                self.fallingThroughPlatformGrace = False
                                self.rect.bottom = platform_left.rect.top + 1
                                self.jump_counter = 2

        # Checking if player is standing on the ground
        if pygame.sprite.spritecollide(ground, playerG, False):
            self.standing = True
            self.falling = False
            self.jumping = False
            self.standingOnPlatform = False
            self.jump_grace = False
            self.fallingThroughPlatformGrace = False
            self.rect.bottom = ground.rect.top
            self.jump_counter = 2


        # Code for jumping and jump grace
        if self.jumping:
            self.standing = False
            self.falling = False
            self.jump_grace = False
            self.standingOnPlatform = False
            self.fallingThroughPlatformGrace = False
            if now - self.jump_start > 200:
                self.jumping = False
                self.jump_grace = True
                self.falling = False
                self.standing = False
                self.standingOnPlatform = False
                self.fallingThroughPlatformGrace = False
        if self.jump_grace:
            self.speedy = 0
            if now - self.jump_start > 250:
                self.jumping = False
                self.falling = False
                self.standing = False
                self.jump_grace = False
                self.standingOnPlatform = False
                self.fallingThroughPlatformGrace = False

        # Code for falling when other things aren't true
        if not self.standing:
            if not self.jumping:
                if not self.jump_grace:
                    if not self.standingOnPlatform:
                        self.falling = True

        if self.falling:  # What happens when you are falling
            self.speedy = 8

        if self.standing:  # What happens when you are standing
            self.speedy = 0

        if self.standingOnPlatform:  # What happens when you are standing on a platform
            self.speedy = 0


        # Moves player depending on speedx and speedy
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # For the cool function im tryna make (EDIT: IT WORKED HOLY EHIY DBSHI FKDFBHGHDF HVGBOJ)
        if self.rect.centerx > WIDTH + WIDTH / 2:
            self.rect.centerx = 0 - WIDTH / 2
        if self.rect.centerx < 0 - WIDTH / 2:
            self.rect.centerx = WIDTH + WIDTH / 2

    # Code that runs when player shoots initially
    def shoot(self):
        global bullet_counter  # To use the global variable

        # Creates a bullet if there are 5 or less bullets on the screen
        if bullet_counter <= 10:  # It's 10 and not 5 because of the going through the side of screen function
            bullet_counter += 1
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            all_sprites.add(bullet)

    # Code that runs when player jumps initially
    def jump(self):
        self.jump_counter -= 1
        self.jump_grace = False
        self.falling = False
        self.standing = False
        self.jumping = True
        self.standingOnPlatform = False
        self.fallingThroughPlatformGrace = False
        self.speedy = -10
        self.jump_start = pygame.time.get_ticks()


class Ground(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Creating sprite
        self.image = pygame.Surface((WIDTH, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.bottom = 720


class Boss(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Creating sprite
        self.image = pygame.Surface((100, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 3

        # Variables
        self.health = 320
        self.down_timeThingy = pygame.time.get_ticks()
        self.side_timeThingy = pygame.time.get_ticks()
        self.down_chargeuptimer = 10000000000000000000000000000000000000000000000
        self.side_chargeuptimer = 10000000000000000000000000000000000000000000000
        self.speedx_variable = 5

        # Booleans
        self.down_attacking = False
        self.side_attacking = False
        self.dead = False

        # This makes the boss move either to left or right on start
        self.speedx_random = random.randrange(1, 3)
        if self.speedx_random == 1:
            self.speedx = 5
        if self.speedx_random == 2:
            self.speedx = -5

    def update(self):
        last_update = pygame.time.get_ticks()

        # If it's been 'amt' seconds since last attack started / start of game, it will attack

        # Down attack
        if last_update - self.down_timeThingy > 8000:
            self.down_chargeup()
            self.down_chargeuptimer = pygame.time.get_ticks()
            self.down_timeThingy = 10000000000000000000000000000000000000000000000

        if last_update - self.down_chargeuptimer > 1000:
            self.down_chargeuptimer = 1000000000000000000000000000000000000
            self.down_attack()
            self.down_timeThingy = pygame.time.get_ticks()

        # Side attack
        if last_update - self.side_timeThingy > 5000:
            self.side_chargeup()
            self.side_chargeuptimer = pygame.time.get_ticks()
            self.side_timeThingy = 10000000000000000000000000000000000000000000

        if last_update - self.side_chargeuptimer > 1000:
            self.side_chargeuptimer = 100000000000000000000000000000000000000
            self.side_attack()
            self.side_timeThingy = pygame.time.get_ticks()

        # If boss has no health, kill the boss
        if self.health <= 0:
            global win
            self.dead = True
            win = True
            self.kill()

        # This chunk of code sets speedx so boss moves side to side
        if self.rect.right >= WIDTH - 5:
            self.speedx = -self.speedx_variable
        if self.rect.left <= 5:
            self.speedx = self.speedx_variable

        if self.health < 150:
            self.speedx_variable = 12

        # Moves boss sideways
        self.rect.x += self.speedx

    def down_attack(self):
        self.down_attacking = True
        # Creates laser
        down_laser = Laser(self.rect.centerx - 5, self.rect.bottom)
        laser_group.add(down_laser)
        all_sprites.add(down_laser)

    def side_attack(self):
        self.side_attacking = True
        # Creates laser
        side_laser = Side_Laser()
        laser_group.add(side_laser)
        all_sprites.add(side_laser)

    def down_chargeup(self):
        # Creates chargeup laser
        down_chargeuplaser = Chargeup_Laser(self.rect.centerx - 5, self.rect.bottom)
        laser_group.add(down_chargeuplaser)
        all_sprites.add(down_chargeuplaser)

    def side_chargeup(self):
        side_chargeuplaser = SideChargeup_Laser()
        all_sprites.add(side_chargeuplaser)


class SideChargeup_Laser(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((10, 50))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        global side_lasery
        global side_laserx

        side_laserx = 0
        side_lasery = 0

        random_numberx = random.randrange(1, 3)
        random_numbery = random.randrange(1, 3)

        if random_numberx == 1:
            side_laserx = 0
            self.rect.left = side_laserx
        if random_numberx == 2:
            side_laserx = WIDTH
            self.rect.right = side_laserx

        if random_numbery == 1:
            side_lasery = 480
            self.rect.centery = side_lasery
        if random_numbery == 2:
            side_lasery = 635
            self.rect.centery = side_lasery

    def update(self):
        if boss.dead:
            self.kill()
        if boss.side_attacking:
            self.kill()


class Chargeup_Laser(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Creating sprite image and rect
        self.image = pygame.Surface((50, 10))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = x
        self.rect.top = y

        # Variables
        self.speedx = boss.speedx

    def update(self):
        if boss.dead:
            self.kill()
        if boss.down_attacking:
            self.kill()
        self.rect.centerx = boss.rect.centerx

class Side_Laser(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global side_lasery
        self.image = pygame.Surface((WIDTH, 60))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.time_thingy = pygame.time.get_ticks()

        self.rect.left = 0
        self.rect.centery = side_lasery

    def update(self):
        last_update = pygame.time.get_ticks()

        # Stops after being shot out for 6 seconds
        if last_update - self.time_thingy > 1000:
            boss.side_attacking = False
            self.kill()

        if boss.dead:
            self.kill()

class Laser(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Creating sprite image and rect
        self.image = pygame.Surface((50, ground.rect.top - boss.rect.bottom))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = x
        self.rect.top = y

        # Variables
        self.speedx = boss.speedx
        self.time_thingy = pygame.time.get_ticks()

    def update(self):
        last_update = pygame.time.get_ticks()

        # Stops after being shot out for 6 seconds
        if last_update - self.time_thingy > 5000:
            boss.down_attacking = False
            self.kill()

        if boss.dead:
            self.kill()

        self.rect.centerx = boss.rect.centerx  # Laser follows the boss


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Creating sprite image and rect
        self.image = pygame.Surface((150, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = x
        self.rect.centery = y


# Creating usable class variables

platform_left = Platform(WIDTH / 3 - 50, HEIGHT * 0.75)  # Creates left platform
platform_right = Platform(50 + (WIDTH * 0.66), HEIGHT * 0.75)  # Creates right platform
boss = Boss()

ground = Ground()
player_start = Player(WIDTH / 2)  # creates the player that you see in the center of the screen on start
player_sides = Player(WIDTH + WIDTH / 2)  # creates off-screen player that is used ot go through the side of the screen

# Creating groups

laser_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
playerG = pygame.sprite.Group()

# Adding things to groups

all_sprites.add(platform_left)
all_sprites.add(platform_right)
all_sprites.add(boss)
all_sprites.add(ground)
all_sprites.add(player_start)
all_sprites.add(player_sides)
platform_group.add(platform_left)
platform_group.add(platform_right)
playerG.add(player_sides)
playerG.add(player_start)
boss_group.add(boss)


running = True
while running:

    last_update = pygame.time.get_ticks()
            # Sets fps
    clock.tick(FPS)

    # Event queue
    for event in pygame.event.get():
        # If player clicks X button(top right), main game loop will close
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Checks if a key is pressed
            if lose or win:
                if event.key == pygame.K_r:
                    bullet_counter = 0
                    win = False
                    lose = False
                    side_lasery = 0
                    side_laserx = 0
                    pygame.sprite.Group.empty(all_sprites)
                    pygame.sprite.Group.empty(laser_group)
                    pygame.sprite.Group.empty(platform_group)
                    pygame.sprite.Group.empty(bullet_group)
                    pygame.sprite.Group.empty(playerG)
                    pygame.sprite.Group.empty(boss_group)
                    platform_left = Platform(WIDTH / 3 - 50, HEIGHT * 0.75)  # Creates left platform
                    platform_right = Platform(50 + (WIDTH * 0.66), HEIGHT * 0.75)  # Creates right platform
                    boss = Boss()

                    ground = Ground()
                    player_start = Player(
                        WIDTH / 2)  # creates the player that you see in the center of the screen on start
                    player_sides = Player(
                        WIDTH + WIDTH / 2)  # creates off-screen player that is used ot go through the side of the screen


                    all_sprites.add(platform_left)
                    all_sprites.add(platform_right)
                    all_sprites.add(boss)
                    all_sprites.add(ground)
                    all_sprites.add(player_start)
                    all_sprites.add(player_sides)
                    platform_group.add(platform_left)
                    platform_group.add(platform_right)
                    playerG.add(player_sides)
                    playerG.add(player_start)
                    boss_group.add(boss)

                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.key == pygame.K_UP:  # If this key is up, run code
                if player_sides.jump_counter > 0 and player_start.jump_counter > 0:  # Jump if able to jump
                    player_sides.jump()
                    player_start.jump()
            if event.key == pygame.K_SPACE:  # If this key is space, shoot
                if not lose:
                    player_sides.shoot()
                    player_start.shoot()

    # Laser collision with player
    if pygame.sprite.groupcollide(playerG, laser_group, False, False):
        # Kills player sprite
        lose = True
        player_sides.kill()
        player_start.kill()

    if pygame.sprite.groupcollide(playerG, boss_group, False, False):
        # Kills player sprite
        lose = True
        player_sides.kill()
        player_start.kill()

    # Bullet collision with boss
    hits = pygame.sprite.groupcollide(bullet_group, boss_group, True, False)
    for i in hits:
        boss.health -= 10
        bullet_counter -= 1

    # Updates all_sprites group

    all_sprites.update()

    screen.fill(BLACK)  # Fills screen with black (covers previous frame)

    if lose:
        draw_text(screen, "YOU ARE LOSE XD", 72, WIDTH / 2, HEIGHT / 2)
    if win:
        draw_text(screen, "YOU ARE WIN", 72, WIDTH / 2, HEIGHT / 2)
    if lose and win:
        draw_text(screen, "TIE", 72, WIDTH / 2, HEIGHT / 2)

    # This is the timer when game ends
    if lose or win:
        draw_text(screen, "Press R to restart", 36, WIDTH / 2, HEIGHT / 1.5)
        draw_text(screen, "Press ESC to exit", 36, WIDTH / 2, HEIGHT / 1.2)

    if not lose:
        if not win:
            draw_boss_healthbar(screen, boss.health * 4)
    all_sprites.draw(screen)  # Draws all_sprites onto screen
    pygame.display.flip()  # Updates whole screen


pygame.quit()
