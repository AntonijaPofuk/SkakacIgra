# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 16:49:26 2018

@author: antonija
"""
import pygame

pygame.init() #inicijalizacija igre
win = pygame.display.set_mode((500,480)) #ekran
ikona = pygame.image.load('standing.png') 
pygame.display.set_icon(ikona)

music = pygame.mixer.music.load('music.mp3') #mora biti izvan funkcije jer inace ne radi
pygame.mixer.music.play(-1)
score = 0
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#font = pygame.font.SysFont('comicsans', 30, True) #Font funkcija, true za bold

def quitGame():
    pygame.quit()
    quit
   
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,w,h))
        if click[0] == 1 and action != None: #na klik 
            action()         
    else:
        pygame.draw.rect(win, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        win.blit(textSurf, textRect)   
        
def ulaz():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        bg1=pygame.image.load('bg2.jpg')
        win.blit(bg1,(0,0))
        
        
        font1 = pygame.font.SysFont('comicsans', 50)
        font2 = pygame.font.SysFont('comicsans', 25)
        
        text = font1.render('Dobrodosli u igru!', 1, (white))
        win.blit(text, (250 - (text.get_width()/2),200))
        
        
        text = font2.render('Pokušajte ubiti sve gobline a da pritom oni ne ubiju Vas....', 1, (white))
        text2=font2.render('Pritisni ESC za izlaz iz igre.''',0,(white))
        win.blit(text, (250 - (text.get_width()/2),440))
        win.blit(text2,(250 - (text2.get_width()/2),455))

        button("START!",91,361,100,50,green,bright_green,igra)
        button("IZLAZ",305,361,100,50,red,bright_red,quitGame)

        pygame.display.update()
        clock.tick(25) #čeka pa izađe
        
        
def igra():      
    pygame.display.set_caption("Prva igra")
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    bg = pygame.image.load('bg.jpg')
    #char = pygame.image.load('standing.png')
    
    bulletSound = pygame.mixer.Sound('bullet.wav')
    hitSound = pygame.mixer.Sound('hit.wav')
     
    score = 0
    
    class player(object):
        def __init__(self,x,y,width,height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 5
            self.isJump = False
            self.left = False
            self.right = False
            self.walkCount = 0
            self.jumpCount = 10
            self.standing = True
            self.hitbox = (self.x + 17, self.y + 11, 29, 52) #rectangle u tuple-u, predsatvlja područje koje mođe biti pogođeno
    
        def draw(self, win):
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
    
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount +=1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    
        def hit(self): #kad se sudare
            self.x = 60
            self.y = 410
            self.walkCount = 0
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('-5', 1, (255,0,0))
            win.blit(text, (250 - (text.get_width()/2),200))
            pygame.display.update()
            i = 0 #odgoda vremena da se vidi ispis
            while i < 200:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 201
                        pygame.quit()
                    
    class projectile(object):
        def __init__(self,x,y,radius,color,facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.facing = facing
            self.vel = 8 * facing
    
        def draw(self,win):
            pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    
    
    class enemy(object):
        walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
        walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
        
        def __init__(self, x, y, width, height, end):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.x, self.end] #ide lijevo pa desno
            self.walkCount = 0
            self.vel = 3
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            self.health = 10
            self.visible = True
      
        def draw(self,win):
            self.move()
            if self.visible:
                if self.walkCount + 1 >= 33:
                    self.walkCount = 0
    
                if self.vel > 0:
                    win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                    self.walkCount += 1
    
                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    
        def move(self): 
            if self.vel > 0: #pikseli startaju od negativnog(L) IDE DESNO
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
    
        def hit(self): 
            
            if self.health > 0:
                self.health -= 1
                
            elif goblin.health == 0 and goblin2.health == 0 :
                bg=pygame.image.load('bg2.jpg')
                font=pygame.font.SysFont('comicsans',50,0,0,None)
                win.blit(bg, (0,0)) #ispunjava pozadinu slikom ne bojom pygame
                text = font.render('Bodovi: ' + str(score), 1, (black)) #kreira ispis
                win.blit(text, (0, 0))  #blit je za pozivanje
                font1 = pygame.font.SysFont('comicsans', 100)
                text = font1.render('Pobjeda!', 1, (black))
                win.blit(text, (250 - (text.get_width()/2),200))
                
                
                while True:
                    for event in pygame.event.get():
                        #print(event)
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    button("Pokušaj ponovno",91,361,150,50,green,bright_green,igra)
                    button("Izlaz",305,361,100,50,red,bright_red,quitGame)
                    pygame.display.update()
                    clock.tick(15) 
           
                #gameDisplay.fill(white) za bijelu pozadinu a ne sliku
                        
                i = 0 #odgoda vremena da se vidi ispis
                while i < 1000:
                    pygame.time.delay(10)
                    i += 1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            i = 301
                            pygame.quit()
                
                pygame.quit()
            else:
                 enemies = []
                 self.visible = False
                 for enemy in enemies[:]:
                     if enemy.visible != True:
                         enemies.remove(enemy)
                     break
                 
                 pygame.display.update()
                                                 
    def redrawGameWindow(): #funkcija za bodove
        win.blit(bg, (0,0)) #ispunjava pozadinu slikom ne bojom pygame
        text = font.render('Bodovi: ' + str(score), 1, (0,0,0)) #kreira ispis
        win.blit(text, (380, 10))  #blit je za pozivanje
        man.draw(win)
        goblin.draw(win)
        goblin2.draw(win)
        for bullet in bullets:
            bullet.draw(win)
        
        pygame.display.update()
        
    #mainloop
    font = pygame.font.SysFont('comicsans', 30, True)
    man = player(200, 410, 64,64)
    goblin = enemy(100, 410, 64, 64, 450)
    goblin2 = enemy(300, 410, 64, 64, 450)
    shootLoop = 0
    bullets = []
    run = True
    while run:
        clock.tick(27)  #FPS 
    
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] and goblin.visible == True:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and goblin.visible == True:
                man.hit()
                score -= 5
        if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1] and goblin2.visible == True:
            if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2] and goblin2.visible == True:
                man.hit()
                score -= 5
                
    
        if shootLoop > 0: #ako imas metke onda povećaj loop
            shootLoop += 1
        if shootLoop > 3:  #ako imas previse metaka smanji loop
            shootLoop = 0
        
        for event in pygame.event.get(): #provjerava događaje pa reagira na njih
            if event.type == pygame.QUIT:
                run = False
            
        for bullet in bullets: #loop za metke
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1] and goblin.visible == True:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and goblin.visible == True:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
            if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1] and goblin2.visible == True:
                if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2] and goblin2.visible == True:
                    hitSound.play()
                    goblin2.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    
                    
            if bullet.x < 500 and bullet.x > 0:  #ne preko ekrana
                bullet.x += bullet.vel  #smjer
            else:
                bullets.pop(bullets.index(bullet)) #ide van ekrana pa se brise metak
    
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
                
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))
    
            shootLoop = 1
            
        if keys[pygame.K_ESCAPE]:
            quitGame()
            
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
            
            
        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
        redrawGameWindow()
    
    pygame.quit()
 
ulaz() #poziva se fulaz pa figra





