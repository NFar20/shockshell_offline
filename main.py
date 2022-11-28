import pygame
import math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    K_MINUS,
    K_EQUALS
)

screen = None
currentPlayer = None
currentProjectile = None
playerOne = None
playerTwo = None
all_sprites = None


class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, speedx, speedy, image):
        super(Projectile, self).__init__()
        # self.surf = pygame.image.load(image).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (10,10))
        self.rect = self.image.get_rect()
        # self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.rect.move_ip(self.x, self.y)

    def move(self, gravity=1):
        # print("vx: "+str(self.speedx))
        # print("vy: "+str(self.speedy))
        # print("(x, y): "+str(self.x)+str(self.y))
        self.x += self.speedx
        self.y += self.speedy
        self.rect.move_ip(self.speedx, self.speedy)
        self.speedy += gravity
        if self.y > 630 or self.x < 0 or self.x > 800:
            print("killed projectile")
            global currentProjectile
            currentProjectile = None

    def checkIntercepts(self):
        # print(self.rect)        
        if self.rect.colliderect(currentPlayer.rect):
            currentPlayer.takeDamage(math.sqrt(self.speedx*self.speedx+self.speedy*self.speedy))
            global currentProjectile
            currentProjectile = None



class Tank(pygame.sprite.Sprite):

    def __init__(self, x, y, launchSpeed, launchAngle, pictureName):
        super(Tank, self).__init__()
        self.health = 100
        self.x = x
        self.y = y
        self.launchSpeed = launchSpeed
        self.launchAngle = launchAngle
        # self.surf = pygame.image.load(pictureName).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.image = pygame.image.load(pictureName)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.dx = 0

    def takeDamage(self, speed):
        self.health -= speed / 3
        # print(self.health)
        if self.health <= 0:
          gameOver(self)

    def adjustStrength(self, upNotDown):
        delta = 0

        if upNotDown:
            delta = 1
        elif not upNotDown:
            delta = -1
        if self.launchSpeed >= 40 and delta > 0:
            return
        if self.launchSpeed <= 20 and delta < 0:
            return
        self.launchSpeed += delta
        print("launch speed is now " + str((self.launchSpeed - 20) * 5) + "%")

    def adjustAngle(self, upNotDown):
        delta = 0

        if upNotDown:
            delta = 1
        else:
            delta = -1
        angle = self.launchAngle + delta
        if self.launchAngle > 90:  # red guy
            if angle > 180 or angle < 100:
                return
        elif angle < 10 or angle > 80:  # blue guy
            return
        self.launchAngle = angle
        print(f"adjusted angle to {self.launchAngle} degrees")

    def move(self, amnt):
        tempdx = self.dx + amnt
        if math.fabs(tempdx) > 100:
            return
        self.x += amnt
        self.dx += amnt
        self.rect.move_ip(amnt, 0)

    def launch(self):
        global currentProjectile
        currentProjectile = Projectile(self.x, self.y, self.launchSpeed * math.cos(self.launchAngle * math.pi / 180),
                                       -self.launchSpeed * math.sin(self.launchAngle * math.pi / 180),
                                       "images\smallTankProjectile.png")


def angleText():
    global font, blueAngle, blueRect, blue, redAngle, redRect, red, playerOne, playerTwo
    blue = (0, 0, 128)
    red = (255, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 32)
    blueAngle = font.render(str(playerOne.launchAngle)+"\u00B0", True, blue)
    redAngle = font.render(str(180-playerTwo.launchAngle)+"\u00B0", True, red)
    blueRect = blueAngle.get_rect()
    redRect = redAngle.get_rect()
    blueRect.center = (100, 200)
    redRect.center = (700, 200)
  
def strengthText():
  global font, blueStrength, blueSRect, redStrength, redSRect, blue, red, playerOne, playerTwo
 
  blueStrength = font.render(str((playerOne.launchSpeed-20)*5)+"%", True, blue)
  redStrength = font.render(str((playerTwo.launchSpeed-20)*5)+"%", True, red)
  blueSRect = blueStrength.get_rect()
  redSRect = redAngle.get_rect()
  blueSRect.center = (100, 300)
  redSRect.center = (700, 300)
  
def background():
    global bg_img
    bg_img = pygame.image.load("images/background.jpeg")
    bg_img = pygame.transform.scale(bg_img, (800,800))
background()

def healthBar():
    global blue, red, screen, playerOne, playerTwo, blueHealthRect, redHealthRect, blueOutlineRect, redOutlineRect, blueHealth, redHealth, blueOutline, redOutline, healthRect
    black = (0, 0, 0)
    if playerOne.health <= 0 or playerTwo.health <= 0:
        return
    blueHealth = pygame.Surface((playerOne.health*2, 20))
    blueHealth.fill(blue)
    redHealth = pygame.Surface((playerTwo.health*2, 20))
    redHealth.fill(red)
    blueOutline = pygame.Surface((200, 20))
    redOutline = pygame.Surface((200, 20))

def gameInit():
    global currentPlayer, playerOne, playerTwo
    playerOne = Tank(100, 600, 40, 45, "images\smallBlueTank.png")
    currentPlayer = playerOne
    playerTwo = Tank(700, 600, 40, 135, "images\smallRedTank.png")


def gameOver(loser):
#   global font
#   winner = None
#   if loser == playerOne:
#     winner  = ("Player two wins!")
#   elif loser == playerTwo:
#     winner = ("Player one wins!")
#   else:
#     print("error")
#   gameOverText = font.render(winner, True, (0, 0, 0))
#   gameOverRect = gameOverText.get_rect()
#   gameOverRect.center = (400, 400)
#   screen.blit(gameOverText, gameOverRect)
#   bg_img = pygame.image.load("images/destroyedtankbackground.jpg")
#   screen.blit(bg_img, (0, 0))
    quit()


def update():
    keys = pygame.key.get_pressed()
    # print("hit Key " + str(keys))
    global currentPlayer, playerOne, playerTwo, blueAngle, blueRect, redAngle, redRect, blueHealthRect, redHealthRect, blueHealth, redHealth, blueOutline, redOutline, healthRect, blueSRect, blueStrength, redSRect, redStrength

    angleText()
    strengthText()
    background()
    healthBar()
    screen.blit(bg_img, (0,0))
    screen.blit(playerOne.image, (playerOne.x, playerOne.y))
    screen.blit(playerTwo.image, (playerTwo.x, playerTwo.y))
    screen.blit(blueAngle, blueRect)
    screen.blit(redAngle, redRect)
    screen.blit(redStrength, redSRect)
    screen.blit(blueStrength, blueSRect)
    screen.blit(blueAngle, blueRect)
    screen.blit(redAngle, redRect)
    screen.blit(blueHealth, (0,700))
    screen.blit(redHealth, (600,700))
    if currentProjectile == None:
        if keys[K_RIGHT]:
            currentPlayer.move(5)
        if keys[K_LEFT]:
            currentPlayer.move(-5)
        if keys[K_UP]:
            currentPlayer.adjustAngle(True)
        if keys[K_DOWN]:
            currentPlayer.adjustAngle(False)
        if keys[K_EQUALS]:
            currentPlayer.adjustStrength(True)
        if keys[K_MINUS]:
            currentPlayer.adjustStrength(False)
        if keys[K_SPACE]:
            currentPlayer.launch()
            if currentPlayer == playerOne:
                currentPlayer = playerTwo
            elif currentPlayer == playerTwo:
                currentPlayer = playerOne
            else:
                print("should not have reached here")

    if currentProjectile != None:
        screen.blit(currentProjectile.image, (currentProjectile.x, currentProjectile.y))
    if currentProjectile != None:
        currentProjectile.checkIntercepts()
    if currentProjectile != None:
        currentProjectile.move()



def gameLoop():
    pygame.init()
    fps = 20
    timer = pygame.time.Clock()

    global screen, playerTwo, playerOne
    screen = pygame.display.set_mode([800, 800])
    pygame.display.set_caption("Shockshell Offline")
    pygame.display.set_icon(pygame.image.load("images/smallBlueTank.png"))
    running = True
    gameInit()
    while running:
        timer.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit")
            elif playerOne.health <= 0 or playerTwo.health <= 0:
                running = False  
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        screen.fill((255, 255, 255))
        update()

        pygame.display.flip()
    pygame.quit()


gameLoop()