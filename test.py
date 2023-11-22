import pygame
import random
import json
from os.path import join
from math import *

class Slimys(pygame.sprite.Sprite):
    MOVEMENT_SPEED = 3

    def __init__(self, pos, scale):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.image.load('Images/slimy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale,self.image.get_height() * scale))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, addSpeed = 0):
        self.y += self.MOVEMENT_SPEED + addSpeed
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Zombie(pygame.sprite.Sprite):
    MOVEMENT_SPEED = 2

    def __init__(self, x, y, zombieType):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

        self.angle = 0
        self.mask = None
        self.rect = None

        self.hit = 0

        self.zombieType = zombieType
        self.health = 0
        self.setHealth(zombieType)

        self.zombieImage = None

    def setHealth(self, zombieType):
        if self.zombieType == 1:
            self.health = 100
        if self.zombieType == 2:
            self.health = 150

    def getImage(self):

        if self.zombieType == 1:
            if self.hit == 0:
                return pygame.image.load('Images/zombieType1.png').convert_alpha()
            elif self.hit == 1:
                return pygame.image.load('Images/Animations/hitEffectZombieType1.png').convert_alpha()

        if self.zombieType == 2:
            if self.hit == 0:
                return pygame.image.load('Images/zombieType2.png').convert_alpha()
            elif self.hit == 1:
                return pygame.image.load('Images/Animations/hitEffectZombieType2.png').convert_alpha()


    def rotate(self, playerPosX, playerPosY):
        self.angle = atan2(-(playerPosY - self.y), playerPosX - self.x)
        self.zombieImage = self.getImage()

        self.width = self.zombieImage.get_width()
        self.height = self.zombieImage.get_height()
        self.zombieImage = pygame.transform.scale(self.zombieImage, (self.width * 2, self.height * 2))
        self.zombieImage = pygame.transform.rotate(self.zombieImage, self.angle*180/pi - 90).convert_alpha()

        self.rect = self.zombieImage.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.zombieImage)

    def move(self, addSpeed = 0):
        self.x += (self.MOVEMENT_SPEED + addSpeed) * cos(self.angle)
        self.y += -(self.MOVEMENT_SPEED + addSpeed) * sin(self.angle)

    def draw(self, screen):
        screen.blit(self.zombieImage, self.rect)

class Bullet(pygame.sprite.Sprite):
    MOVEMENT_SPEED = 20

    def __init__(self, x, y, rotationX, rotationY):
        super().__init__()
        self.x = x
        self.y = y
        self.bulletImage = pygame.image.load("Images/bullet.png").convert_alpha()
        self.bulletImage = pygame.transform.scale2x(self.bulletImage)
        self.angle = 0
        self.rect = None

        self.rotate(rotationX, rotationY)
        self.centerlize()

    def centerlize(self):
        self.x += -16 * cos(self.angle + pi/2)
        self.y += 18 * sin(self.angle + pi/2)
        self.x += 80 * cos(self.angle)
        self.y += -80 * sin(self.angle)

    def rotate(self, rotationX, rotationY):
        self.angle = (atan2(-(rotationY - self.y), rotationX - self.x))
        self.bulletImage = pygame.transform.rotate(self.bulletImage, self.angle*180/pi - 90)

        self.mask = pygame.mask.from_surface(self.bulletImage)

    def move(self):
        self.x += self.MOVEMENT_SPEED * cos(self.angle)
        self.y += -self.MOVEMENT_SPEED * sin(self.angle)

    def draw(self, screen):
        self.rect = self.bulletImage.get_rect(center=(self.x, self.y))
        screen.blit(self.bulletImage, self.rect)

class Player(pygame.sprite.Sprite):
    MOVEMENT_SPEED = 5

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.playerImage = None

        self.rect = None
        self.mask = None

    def draw(self, screen):
        screen.blit(self.playerImage, self.rect)

    def rotate(self, mousePosX, mousePosY):
        angle = (atan2(-(mousePosY - self.y), mousePosX - self.x))*180/pi

        self.playerImage = pygame.image.load("Images/soldier.png").convert_alpha()
        self.playerImage = pygame.transform.rotate(self.playerImage, angle - 90 - 180)

        self.rect = self.playerImage.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.playerImage)

    def getWidth(self):
        return self.playerImage.get_width()

    def getHeight(self):
        return self.playerImage.get_height()

    def move(self):
        userAction = pygame.key.get_pressed()

        if userAction[pygame.K_d]:
            self.x += self.MOVEMENT_SPEED
        if userAction[pygame.K_w]:
            self.y -= self.MOVEMENT_SPEED
        if userAction[pygame.K_s]:
            self.y += self.MOVEMENT_SPEED
        if userAction[pygame.K_a]:
           self.x -= self.MOVEMENT_SPEED

class Text():
    def __init__(self, text, font, fontSize, x, y, color = (190, 190, 190)):
        self.x = x
        self.y = y

        self.text = text
        self.font = pygame.font.SysFont(font, fontSize)
        self.img = self.font.render(self.text, True, color)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Button():
    def __init__(self, x, y, buttonName, scale, screen):

        self.screen = screen

        self.x = x
        self.y = y
        self.scale = scale
        self.buttonName = buttonName

        self.image = self.getNormalImage()

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(),self.image.get_height())

        self.pressed = False
        self.mousePressed = True

    #     --------------------------------

    def getWidth(self):
        return self.image.get_width()

    def getHeight(self):
        return self.image.get_height()

    def changePos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def getHoverImage(self):
        image = pygame.image.load(join('Images', 'Buttons', 'Animations', self.buttonName + 'Hovered' + '.png')).convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))

        return image

    def getNormalImage(self):
        image = pygame.image.load(join('Images', 'Buttons', self.buttonName + '.png')).convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))

        return image


    def checkPressed(self):
        mousePos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(mousePos):
            self.image = self.getHoverImage()

            if pygame.mouse.get_pressed()[0] == 1 and (not self.pressed):
                self.pressed = True
                action = True
        else:
            self.image = self.getNormalImage()


        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False


        return action

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class LevelButton(Button):
    def __init__(self, x, y, buttonName, scale, screen, lvl, text = ''):
        super().__init__(x, y, buttonName, scale, screen)

        self.text = Text(text, 'arialblack', 24, 100, 300)
        self.lvl = lvl

        self.image = self.getDarkenImage()

        self.canBePressed = False

    def getDarkenImage(self):
        image = pygame.image.load(join('Images', 'Buttons', 'Animations', self.buttonName + 'Darken' + '.png')).convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))

        return image

    def checkPressed(self, lvlAchived):
        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos):
            if lvlAchived >= self.lvl:
                self.text.draw(self.screen)
                self.image = self.getHoverImage()
                if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                    self.pressed = True
                    return True
        else:
            if lvlAchived >= self.lvl:
                self.image = self.getNormalImage()
            else:
                self.image = self.getDarkenImage()

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False


class Game():
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 1000
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Zombie Crasher")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.playBtn = Button(0, 200, 'playButton', 4, self.screen)
        self.exitBtn = Button(0,350, 'exitButton', 4, self.screen)
        self.resumeBtn = Button(0,200,'resumeButton', 4, self.screen)
        self.storyBtn = Button(0,200,'storyButton', 4, self.screen)

        self.lvl1Button = LevelButton(100,200, 'lvl1Button', 4, self.screen, 1, text = 'This is an easy level')
        self.lvl2Button = LevelButton(200,200, 'lvl2Button', 4, self.screen, 2, text = 'This is a harder level')

        self.state = 'mainMenu'
        self.statelvl = None

        self.levelZombiesCount = {
            'lvl1' : 20,
            'lvl2' : 30,
        }

        self.lvlAch = 1

        try:
            with open('lvlsSaving.txt') as lvlsSaving:
                self.lvlAch = json.load(lvlsSaving)
        except:
            pass

        self.run = True

        self.bullets = []

        self.lastUpdate = pygame.time.get_ticks()

        self.zombieX = 66
        self.zombieY = 66

        self.player = Player(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)

        self.zombies = []
        self.slimys = []

        self.pressed = True


    def zombieAndBulletCollisions(self, bullets, zombies, currentTime, lastUpdate):

        if currentTime - lastUpdate >= 500:
            lastUpdate = currentTime
            for zombie in zombies:
                zombie.hit = 0

        for bullet in bullets:
            countZombies = 0
            for zombie in zombies:
                if pygame.sprite.collide_mask(bullet, zombie) and countZombies == 0:
                    zombie.health -= 50
                    bullets.pop(bullets.index(bullet))
                    countZombies += 1
                    zombie.hit = 1
                    break
                elif countZombies >= 1:
                    break


        return lastUpdate

    def checkHealth(self, zombies, state):

        for zombie in zombies:
            if zombie.health <= 0:
                zombies.pop(zombies.index(zombie))
                self.levelZombiesCount[state] -= 1

    def bulletsOutOfScreen(self, bullets):
        for bullet in bullets:
            if bullet.x >= self.SCREEN_WIDTH + 10 or bullet.x <= -10:
                bullets.pop(bullets.index(bullet))
            elif bullet.y >= self.SCREEN_HEIGHT + 10 or bullet.y <= -10:
                bullets.pop(bullets.index(bullet))

    def slimysOutOfScreen(self, slimys):
        for slimy in slimys:
            if slimy.y >= self.SCREEN_HEIGHT:
                slimys.pop(slimys.index(slimy))

    def spawnSlimys(self, slimys):

        scale = 2
        slimyImage = pygame.image.load('Images/slimy.png')
        slimyImageHeight = pygame.image.load('Images/slimy.png').get_height() * scale
        slimyImageWidth = pygame.image.load('Images/slimy.png').get_width() * scale

        spawnPoints = {1: (0 * slimyImageWidth, -slimyImageHeight),
                       2: (1 * slimyImageWidth, -slimyImageHeight),
                       3: (2 * slimyImageWidth, -slimyImageHeight),
                       4: (3 * slimyImageWidth, -slimyImageHeight),
                       5: (4 * slimyImageWidth, -slimyImageHeight),
                       6: (5 * slimyImageWidth, -slimyImageHeight),
                       7: (6 * slimyImageWidth, -slimyImageHeight),
                       8: (7 * slimyImageWidth, -slimyImageHeight),
                       9: (8 * slimyImageWidth, -slimyImageHeight)
        }

        if random.randint(1,1000) % 300 == 0:
            slimys.append(Slimys(spawnPoints[random.randint(1,9)], scale))

    def spawnZombies(self, zombies):

        zombieImage = pygame.image.load('Images/zombieType1.png')
        zombieImageHeight = zombieImage.get_height()
        zombieImageWidth = zombieImage.get_width()

        spawnPoints = {1: (-zombieImageWidth, -zombieImageHeight),
                       2: (self.SCREEN_WIDTH/2, -zombieImageHeight),
                       3: (self.SCREEN_WIDTH + zombieImageWidth, -zombieImageHeight),
                       4: (-zombieImageWidth, self.SCREEN_HEIGHT/2),
                       5: (self.SCREEN_WIDTH + zombieImageWidth, self.SCREEN_HEIGHT/2),
                       6: (-zombieImageWidth, self.SCREEN_HEIGHT + zombieImageHeight),
                       7: (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT + zombieImageHeight),
                       8: (self.SCREEN_WIDTH + zombieImageWidth, self.SCREEN_HEIGHT + zombieImageHeight)
        }

        rand = random.randint(1,1000)

        if rand % 100 == 0 and rand % 400 != 0:
            randNum = random.randint(1,8)
            zombies.append(Zombie(spawnPoints[randNum][0], spawnPoints[randNum][1], 1))
        elif rand % 400 == 0:
            randNum = random.randint(1,8)
            zombies.append(Zombie(spawnPoints[randNum][0], spawnPoints[randNum][1], 2))

    def deathCondition(self, player, slimys, zombies):

        for slimy in slimys:
            if pygame.sprite.collide_mask(player, slimy):
                return False

        for zombie in zombies:
            if pygame.sprite.collide_mask(player, zombie):
                return False


        return True

    def setToDefaults(self):
        self.slimys = []
        self.zombies = []
        self.bullets = []
        self.player.x = self.SCREEN_WIDTH / 2
        self.player.y = self.SCREEN_HEIGHT / 2
        self.levelZombiesCount = {
            'lvl1' : 20,
            'lvl2' : 30,
        }

    def playerOutOfScreen(self):
        if self.player.x >= self.SCREEN_WIDTH + self.player.getWidth()/2 + 10 or self.player.x <= -10 - self.player.getWidth():
            return True
        if self.player.y >= self.SCREEN_HEIGHT + self.player.getHeight()/2 + 10 or self.player.y <= -10 - self.player.getHeight():
            return True

    def gameProcces(self):
        while self.run:


            if self.state == 'mainMenu':

                self.setToDefaults()

                self.screen.fill((50,50,50))

                self.playBtn.changePos(self.SCREEN_WIDTH/2 - self.playBtn.getWidth()/2, 200)
                self.storyBtn.changePos(self.SCREEN_WIDTH/2 - self.storyBtn.getWidth()/2, 300)
                self.exitBtn.changePos(self.SCREEN_WIDTH/2 - self.exitBtn.getWidth()/2, 400)


                self.playBtn.draw()
                self.storyBtn.draw()
                self.exitBtn.draw()

                if self.playBtn.checkPressed():
                    self.state = 'levels'
                if self.storyBtn.checkPressed():
                    self.state = 'story'
                if self.exitBtn.checkPressed():
                    self.run = False

            elif self.state == 'story':
                self.screen.fill((50,50,50))

                self.setToDefaults()

                self.exitBtn.changePos(10, self.SCREEN_HEIGHT - self.exitBtn.getHeight() - 10)
                self.exitBtn.draw()

                text = Text('Zombie Crasher', 'arialblack', 44, 10, 10, (89, 158, 89))
                text.draw(self.screen)

                text = Text('(Нотатки 2136 року)', 'arialblack', 20, 10, 100, (89, 158, 89))
                text.draw(self.screen)

                text = Text('Світ охопила епідемія… Люди не могли знайти ліки від цієї хвороби, тому їм', 'arialblack', 20, 10, 120, (89, 158, 89))
                text.draw(self.screen)

                text = Text('прийшлося боротися. Люди після зараження ставали неконтрольованими,', 'arialblack', 20, 10, 140, (89, 158, 89))
                text.draw(self.screen)

                text = Text('вони не слухалися… Таких людей ми назвали зомбі. Вони мертві, але живі.', 'arialblack', 20, 10, 160, (89, 158, 89))
                text.draw(self.screen)

                text = Text('Це лякає.', 'arialblack', 20, 10, 180, (160, 10, 0))
                text.draw(self.screen)

                text = Text('На одній з ваших вилазок вам не пощастило, ви наткнулися на натовп зомбі.', 'arialblack', 20, 10, 220, (89, 158, 89))
                text.draw(self.screen)

                text = Text('Вони йдуть, скоріше діставайте зброю!', 'arialblack', 20, 10, 240, (89, 158, 89))
                text.draw(self.screen)

                text = Text('На вашому шляху зустрінуться  такі істоти:', 'arialblack', 20, 10, 300, (89, 158, 89))
                text.draw(self.screen)

                zombieType1Img = pygame.image.load('Images/zombieType1.png')
                zombieType1Img = pygame.transform.scale(zombieType1Img, (zombieType1Img.get_width() * 2, zombieType1Img.get_height() * 2))
                zombieType2Img = pygame.image.load('Images/zombieType2.png')
                zombieType2Img = pygame.transform.scale(zombieType2Img, (zombieType2Img.get_width() * 2, zombieType2Img.get_height() * 2))
                slimyImg  = pygame.image.load('Images/slimy.png')
                slimyImg = pygame.transform.scale(slimyImg, (slimyImg.get_width() * 2, slimyImg.get_height() * 2))

                self.screen.blit(zombieType1Img, (100, 340))
                self.screen.blit(zombieType2Img, (zombieType1Img.get_width() + 300, 340))
                self.screen.blit(slimyImg, (zombieType1Img.get_width() + zombieType2Img.get_width() + 800, 340))

                text = Text('Цей вид зомбі найслабший,', 'arialblack', 16, 10, 340 + zombieType1Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('йому вистачає 2 патрони.', 'arialblack', 16, 10, 356 + zombieType1Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('Цей вже сильніший. Він пробув', 'arialblack', 16, zombieType1Img.get_width() + 250, 340 + zombieType2Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('зараженим більше часу, ніж попередній,', 'arialblack', 16, zombieType1Img.get_width() + 250, 356 + zombieType2Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('тому його шкіра покрилася світлою ', 'arialblack', 16, zombieType1Img.get_width() + 250, 372 + zombieType2Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('біологічною бронею. Такий з’їсть більше пуль.', 'arialblack', 16, zombieType1Img.get_width() + 250, 388 + zombieType2Img.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('А це Слимак. Так називаємо його ми. ', 'arialblack', 16, zombieType1Img.get_width() + zombieType2Img.get_width() + 650, 340 + slimyImg.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('Патрони його не беруть і живе він під ', 'arialblack', 16, zombieType1Img.get_width() + zombieType2Img.get_width() + 650, 356 + slimyImg.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)

                text = Text('землею, тому від нього ми можемо тільки тікати.', 'arialblack', 16, zombieType1Img.get_width() + zombieType2Img.get_width() + 650, 372 + slimyImg.get_height() + 20, (150, 142, 86))
                text.draw(self.screen)


                text = Text('Управління:', 'arialblack', 24, 10, 450 + slimyImg.get_height() + 20, (89, 158, 89))
                text.draw(self.screen)

                text = Text('ЛКМ – стрільба', 'arialblack', 16, 10, 490 + slimyImg.get_height() + 20, (89, 158, 89))
                text.draw(self.screen)

                text = Text('W, A, S, D – рухатися', 'arialblack', 16, 10, 506 + slimyImg.get_height() + 20, (89, 158, 89))
                text.draw(self.screen)

                text = Text('Поворот миші – цілитися', 'arialblack', 16, 10, 522 + slimyImg.get_height() + 20, (89, 158, 89))
                text.draw(self.screen)


                if self.exitBtn.checkPressed():
                    self.state = 'mainMenu'

            elif self.state == 'levels':
                self.setToDefaults()


                self.screen.fill((50,50,50))

                self.lvl1Button.changePos(100, 200)
                self.lvl2Button.changePos(200, 200)
                self.exitBtn.changePos(100, 350)


                self.lvl1Button.draw()
                self.lvl2Button.draw()
                self.exitBtn.draw()

                if self.lvl1Button.checkPressed(self.lvlAch):
                    self.state = 'lvl1'
                if self.lvl2Button.checkPressed(self.lvlAch):
                    self.state = 'lvl2'
                if self.exitBtn.checkPressed():
                    self.state = 'mainMenu'

            elif self.state == 'youWonMenu':

                self.setToDefaults()

                currentTime = pygame.time.get_ticks()
                self.screen.fill((100,100,100))
                text = Text('You won!!!', 'arialblack', 30, 635,400, (162, 227, 66))
                text.draw(self.screen)

                if currentTime - self.lastUpdate >= 3000:
                    self.state = 'mainMenu'

            elif self.state == 'youLoseMenu':
                self.setToDefaults()

                currentTime = pygame.time.get_ticks()
                self.screen.fill((100,100,100))
                text = Text('You are dead!!!', 'arialblack', 30, 635,400, (170, 10, 10))
                text.draw(self.screen)

                if currentTime - self.lastUpdate >= 3000:
                    self.state = 'mainMenu'

            elif self.state == 'pause':
                self.screen.fill((50,50,50))

                self.resumeBtn.changePos(self.SCREEN_WIDTH/2 - self.playBtn.getWidth()/2, 250)
                self.exitBtn.changePos(self.SCREEN_WIDTH/2 - self.playBtn.getWidth()/2, 350)

                self.resumeBtn.draw()
                self.exitBtn.draw()

                self.pressed = True

                if self.resumeBtn.checkPressed():
                    self.state = self.statelvl
                if self.exitBtn.checkPressed():
                    self.state = 'mainMenu'

            elif self.state == 'lvl1':

                if self.levelZombiesCount['lvl1'] <= 0:
                    self.lvlAch = 2

                    with open('lvlsSaving.txt', 'w') as lvlsSaving:
                        json.dump(self.lvlAch, lvlsSaving)

                    self.state = 'youWonMenu'

                self.statelvl = 'lvl1'
                self.screen.fill((100,100,100))

                pos = pygame.mouse.get_pos()

                #collisions
                currentTime = pygame.time.get_ticks()
                self.lastUpdate = self.zombieAndBulletCollisions(self.bullets, self.zombies, currentTime , self.lastUpdate)
                self.checkHealth(self.zombies, self.state)

                self.spawnSlimys(self.slimys)
                self.spawnZombies(self.zombies)

                #rotation
                self.player.rotate(pos[0], pos[1])
                for zombie in self.zombies:
                    zombie.rotate(self.player.x, self.player.y)

                #movement part
                self.player.move()

                for zombie in self.zombies:
                    zombie.move()

                for bullet in self.bullets:
                    bullet.move()

                for slimy in self.slimys:
                    slimy.move()

                if not self.deathCondition(self.player, self.slimys, self.zombies):
                    self.state = 'youLoseMenu'

                # out of screen
                if self.playerOutOfScreen():
                    self.state = 'youLoseMenu'

                self.bulletsOutOfScreen(self.bullets)
                self.slimysOutOfScreen(self.slimys)

                if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                    self.pressed = True
                    pos = pygame.mouse.get_pos()
                    self.bullets.append(Bullet(self.player.x, self.player.y, pos[0], pos[1]))

                if pygame.mouse.get_pressed()[0] == 0:
                    self.pressed = False

                self.clock.tick(70)

                #drawing objects on screen
                for slimy in self.slimys:
                    slimy.draw(self.screen)

                for bullet in self.bullets:
                    bullet.draw(self.screen)

                self.player.draw(self.screen)

                for zombie in self.zombies:
                    zombie.draw(self.screen)

                text = Text('Zombies left: {0}'.format(self.levelZombiesCount[self.statelvl]), 'arialblack', 30, 0, 0, (38, 231, 237))
                text.draw(self.screen)

            elif self.state == 'lvl2':

                self.statelvl = 'lvl2'

                self.screen.fill((91, 125, 40))

                if self.levelZombiesCount['lvl2'] <= 0:
                    self.state = 'youWonMenu'

                pos = pygame.mouse.get_pos()

                #collisions
                currentTime = pygame.time.get_ticks()
                self.lastUpdate = self.zombieAndBulletCollisions(self.bullets, self.zombies, currentTime , self.lastUpdate)
                self.checkHealth(self.zombies, self.state)

                self.spawnSlimys(self.slimys)
                self.spawnZombies(self.zombies)

                #rotation
                self.player.rotate(pos[0], pos[1])
                for zombie in self.zombies:
                    zombie.rotate(self.player.x, self.player.y)

                #movement part
                self.player.move()

                for zombie in self.zombies:
                    zombie.move(1)

                for bullet in self.bullets:
                    bullet.move()

                for slimy in self.slimys:
                    slimy.move(2)

                # death condition
                if not self.deathCondition(self.player, self.slimys, self.zombies):
                    self.state = 'youLoseMenu'

                # out of screen
                if self.playerOutOfScreen():
                    self.state = 'youLoseMenu'
                self.bulletsOutOfScreen(self.bullets)
                self.slimysOutOfScreen(self.slimys)

                if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                    self.pressed = True
                    pos = pygame.mouse.get_pos()
                    self.bullets.append(Bullet(self.player.x, self.player.y, pos[0], pos[1]))

                if pygame.mouse.get_pressed()[0] == 0:
                    self.pressed = False

                self.clock.tick(70)

                #drawing objects on screen
                for slimy in self.slimys:
                    slimy.draw(self.screen)

                for bullet in self.bullets:
                    bullet.draw(self.screen)

                self.player.draw(self.screen)

                for zombie in self.zombies:
                    zombie.draw(self.screen)

                text = Text('Zombies left: {0}'.format(self.levelZombiesCount[self.statelvl]), 'arialblack', 30, 0, 0, (38, 231, 237))
                text.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and (self.state == 'lvl1' or self.state == 'lvl2'):
                        self.state = 'pause'

            #update screen
            pygame.display.flip()

def main():
    game = Game()
    game.gameProcces()
    pygame.quit()

if __name__ == "__main__":
    main()
