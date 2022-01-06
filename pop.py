# Jonathan Carter
# Game1-animated Player
# 12/10/2021
# All assets are from https://kenney.nl/

# Imports
import pygame
import random

# Buttons
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_LSHIFT,
    K_SPACE,
    QUIT,
)

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Player class


class Player(pygame.sprite.Sprite):
    movecount = 0
    ismoving = False
    speed = 10
    level = 1

    def setmoving(self, value):
        self.ismoving = value

    def increasespeed(self, increase):
        self.speed += increase

    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("assets/ships.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH / 2),
                (SCREEN_HEIGHT - 64),
            )
        )

    def update(self, pressed__keys):  # I had to make the animation for the flame myself so it's a tiny bit jank
        playeranimation = ["assets/ships.png", "assets/ships1.png", "assets/ships2.png", "assets/ships3.png", "assets/ships2.png", "assets/ships1.png"]
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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Enemy Class
class enemy1(pygame.sprite.Sprite):
    moveCount = 0

    def __init__(self):
        super(enemy1, self).__init__()
        self.surf = pygame.image.load("assets/E1Ships.png")
        self.rect = self.surf.get_rect(
            center=(
                random.randint(5, SCREEN_WIDTH - 10),
                random.randint(1, 10),
            ))
        self.speed = random.randint(4, 10)
        self.etype = "fodder"

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.bulletCount = 0
        self.item = random.choice(["bullet"])
        if self.item == "bullet":
            self.etype = "bullet"

        if self.etype == "bullet":
            self.surf = pygame.image.load("assets/basicfires.png")
            self.rect = self.surf.get_rect(
                center=(player.rect.left + 33, player.rect.bottom - 50),)
        self.speed = 5

    def update(self):
        print("In update")
        bulletimage = "assets/basicfires.png"
        print(self.etype)
        if self.etype == "bullet":
            self.surf = pygame.image.load(bulletimage).convert_alpha()
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip(0, - self.speed)


# Starts pygame and makes some variables
pygame.init()
lives = 4
black = (0, 0, 0)
red = 178
green = 190
blue = 181
myFont = pygame.font.SysFont("Comicsans", 40)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Battle")

# Spawning enemies
ADDPLANE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPLANE, 1000)

player = Player()

# The groups
all_sprites = pygame.sprite.Group()
plane_sprites = pygame.sprite.Group()
weapon_sprites = pygame.sprite.Group()
all_sprites.add(player)

# The loop
running = True
bulletcount = 30
while running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT or event.key == K_RIGHT:
                player.setmoving(False)
            if event.key == K_LSHIFT:
                if bulletcount > 0:
                    # bulletcount -= 1          later I want to add ammo pickups an a limited bullet amount
                    weapon = Projectile()
                    weapon_sprites.add(weapon)
                    all_sprites.add(weapon_sprites)
                    # sound to be added

        if event.type == ADDPLANE:
            newplane = enemy1()
            plane_sprites.add(newplane)
            all_sprites.add(newplane)

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    plane_sprites.update()
    weapon_sprites.update()

    screen.fill((red, green, blue))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    pygame.display.flip()

    clock.tick(30)
