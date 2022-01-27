# Jonathan Carter
# First Game
# 1/13/2022
# All assets are from https://kenney.nl/

import random

# Imports
import pygame
# Buttons
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_LSHIFT,
    QUIT,
    K_LCTRL,
)

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):
    movecount = 0
    ismoving = False
    speed = 10
    level = 1
    bulletcount = 5

    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("./assets/ships.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH / 2),
                (SCREEN_HEIGHT - 64),
            )
        )

    def update(self, pressed__keys):  # I had to make the animation for the flame myself so it's a tiny bit jank
        playeranimation = ["./assets/ships.png", "./assets/ships1.png", "./assets/ships2.png", "./assets/ships3.png",
                           "./assets/ships2.png", "./assets/ships1.png"]
        if self.movecount > len(playeranimation) - 1:
            self.movecount = 0
        self.surf = pygame.image.load(playeranimation[self.movecount]).convert_alpha()
        self.movecount += 1

        # Movement
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)

        if pressed_keys[K_LCTRL]:
            self.speed = 5
        else:
            self.speed = 10

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def bulletfire(self):
        self.bulletcount -= 1

    def setmoving(self, value):
        self.ismoving = value

    def increasespeed(self, increase):
        self.speed += increase

    def addbullets(self, nbullets):
        self.bulletcount += nbullets


class enemy1(pygame.sprite.Sprite):
    moveCount = 0
    isdying = False

    def __init__(self):
        super(enemy1, self).__init__()
        self.surf = pygame.image.load("./assets/E1Ships.png")
        self.rect = self.surf.get_rect(
            center=(
                random.randint(5, SCREEN_WIDTH - 10),
                random.randint(1, 10),
            ))
        self.speed = random.randint(4, 10)
        self.etype = "fodder"
        self.diecount = 30

    def update(self):
        if not self.isdying:
            self.rect.move_ip(0, 5)
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()
        else:
            if self.diecount == 0:
                self.kill()
            else:
                deathrand = random.randint(1, 3)
                if deathrand == 1:
                    self.surf = pygame.image.load("./assets/death1.png")
                if deathrand == 2:
                    self.surf = pygame.image.load("./assets/death2.png")
                if deathrand == 3:
                    self.surf = pygame.image.load("./assets/death3.png")
                self.diecount -= 1


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.surf = pygame.image.load("./assets/basicfires.png")
        self.rect = self.surf.get_rect(
                center=(player.rect.left + 33, player.rect.bottom - 50), )
        self.speed = 5

    def update(self):
        bulletimage = "./assets/basicfires.png"
        self.surf = pygame.image.load(bulletimage).convert_alpha()
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip(0, - self.speed)


class powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(powerup, self).__init__()

        poweruproll = random.randint(1, 100)
        if poweruproll <= 50:
            self.surf = pygame.image.load("./assets/bullet1powerup.png")
            self.bulletup = 1
        elif 50 < poweruproll < 80:
            self.surf = pygame.image.load("./assets/bullet2powerup.png")
            self.bulletup = 2
        elif poweruproll >= 80:
            self.surf = pygame.image.load("./assets/bullet3powerup.png")
            self.bulletup = 3
        else:
            print("error in poweruproll")
            print(poweruproll)
            self.surf = pygame.image.load("./assets/bullet1powerup.png")
            self.bulletup = 1

        self.rect = self.surf.get_rect(
            center=(
                random.randint(5, SCREEN_WIDTH - 10),
                random.randint(1, 10),
            ))
        self.speed = random.randint(1, 10)

    def getat(self):
        return self.bulletup

    def update(self):
        self.rect.move_ip(0, + self.speed)
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


# Starts pygame and makes some variables
pygame.init()
black = (0, 0, 0)
red = 178
green = 190
blue = 181
score = 0
bulletcounter = 5
myFont = pygame.font.SysFont("Comicsans", 25)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Battle")

# Spawning enemies
ADDPLANE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPLANE, 400)

player = Player()

# The groups
all_sprites = pygame.sprite.Group()
plane_sprites = pygame.sprite.Group()
weapon_sprites = pygame.sprite.Group()
powerup_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
all_sprites.add(player)
player_sprite.add(player)

# The loop
running = True
while running:
    for event in pygame.event.get():

        # Controls
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT or event.key == K_RIGHT:
                player.setmoving(False)
            if event.key == K_LSHIFT:
                if player.bulletcount > 0:
                    player.bulletfire()
                    bulletcounter = player.bulletcount
                    weapon = Projectile()
                    weapon_sprites.add(weapon)
                    all_sprites.add(weapon_sprites)
                    # sound to be added

        # Spawns the basic plane and powerup
        if event.type == ADDPLANE:
            newplane = enemy1()
            plane_sprites.add(newplane)
            all_sprites.add(newplane)
            roll = random.randint(1, 10)
            if bulletcounter == 0:
                roll += 3
            if roll >= 10:
                Powerup = powerup()
                powerup_sprites.add(Powerup)
                all_sprites.add(Powerup)

        # Quits
        elif event.type == QUIT:
            running = False

    # Gets the keys and updates groups
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    plane_sprites.update()
    weapon_sprites.update()
    powerup_sprites.update()

    # Draws the screen
    screen.fill((red, green, blue))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Makes the bullet collisions
    for entity in weapon_sprites:
        newplane = pygame.sprite.spritecollideany(entity, plane_sprites)
        if newplane is not None:
            if newplane.isdying:
                pass
            else:
                entity.kill()
                score += 5
                newplane.isdying = True

    # Makes the powerup collisions
    for entity in powerup_sprites:
        Powerup = pygame.sprite.spritecollideany(entity, player_sprite)
        if Powerup is not None:
            awardType = entity.getat()
            if awardType == 1:
                player.addbullets(3)
                score += 3
            elif awardType == 2:
                player.addbullets(5)
                score += 5
            elif awardType == 3:
                player.addbullets(10)
                score += 10
            bulletcounter = player.bulletcount
            entity.kill()

    # Displays score
    scorelabel = myFont.render("Score:", True, black)
    scorevalue = myFont.render(str(score), True, black)
    screen.blit(scorelabel, (SCREEN_WIDTH - 250, 2))
    screen.blit(scorevalue, (SCREEN_WIDTH - 150, 2))

    # Displays the bullet counter
    if bulletcounter <= 5:
        bulletimg = pygame.image.load("assets/bullet1.png")
    elif 5 <= bulletcounter < 10:
        bulletimg = pygame.image.load("assets/bullet2.png")
    elif bulletcounter >= 10:
        bulletimg = pygame.image.load("assets/bullet3.png")
    else:
        bulletimg = pygame.image.load("assets/bullet1.png")
    screen.blit(bulletimg, (SCREEN_WIDTH - 600, 2))
    bulletdisplay = myFont.render(str(bulletcounter), True, black)
    screen.blit(bulletdisplay, (SCREEN_WIDTH - 560, 2))

    pygame.display.flip()

    clock.tick(30)
