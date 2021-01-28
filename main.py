import pygame

pygame.init() #you need to initialize always the pygame

win = pygame.display.set_mode((500, 480))  #this is our window and the size of the window
pygame.display.set_caption('First Game')  #this is to display the window

#loading the images of the character
# pygame.image.load(pygame.path.join('nameofthefolder', 'R1.png') to choose another folder where the images are
#or simply pygame.image.load('Game/R1.png')
walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')

clock = pygame.time.Clock() #this will allow us to change our FPS in the game

#SOUND!!
bulletSound = pygame.mixer.Sound('Game/bullet.wav') #to load the sound effect
#bulletSound.play()  #to play it
hitSound = pygame.mixer.Sound('Game/hit.wav')
music = pygame.mixer.music.load('Game/music.mp3') #to load the main music
pygame.mixer.music.play(-1) #to play the main music, the -1 will continue play it in loop.

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #we have a tuple with 4 things, its the rectangle which goes around our character



    def draw(self, win):
        if self.walkCount + 1 >= 27:  # for display the character 3 times per image per frame, we have 9 images and we want to show 3 times each per frame
            self.walkCount = 0


        if not(self.standing): #if he is not standing, it means if he is moving then we will be moving left or right
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        #check weather he is standing or he is moving
        else:
            if self.right:
                win.blit(walkRight[0], (self.x , self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #we have to draw it everytime that we draw the character, so this is why we put it here
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #this is to show the hitbox around the player

    def hit(self):
        self.isJump = False #we need to add this variables on the method hit otherwise after the man is being hit the character will continue 'jumping'
        self.jumpCount = 10 #we need to add this variables on the method hit otherwise after the man is being hit the character will continue 'jumping'
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update() #this will display
        # we want to pause the character for few seconds when it get hitted
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            #we wanna make sure that we can exit the game while its delaying, otherwise we will need to wait that the delay is done and then we will be able to close the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing #this will determinate if the projectile is moving left or right.
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('Game/R1E.png'), pygame.image.load('Game/R2E.png'), pygame.image.load('Game/R3E.png'), pygame.image.load('Game/R4E.png'), pygame.image.load('Game/R5E.png'), pygame.image.load('Game/R6E.png'), pygame.image.load('Game/R7E.png'), pygame.image.load('Game/R8E.png'), pygame.image.load('Game/R9E.png'), pygame.image.load('Game/R10E.png'), pygame.image.load('Game/R11E.png')]
    walkLeft = [pygame.image.load('Game/L1E.png'), pygame.image.load('Game/L2E.png'), pygame.image.load('Game/L3E.png'), pygame.image.load('Game/L4E.png'), pygame.image.load('Game/L5E.png'), pygame.image.load('Game/L6E.png'), pygame.image.load('Game/L7E.png'), pygame.image.load('Game/L8E.png'), pygame.image.load('Game/L9E.png'), pygame.image.load('Game/L10E.png'), pygame.image.load('Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end] #this is the path that our enemy has
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33: #33 images becuase the enemy has 11 pics to the left and 11 to the right for the animation
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y+2, 31, 57)

            #helthbar
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10 ))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(10 - self.health)), 10))
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) This is to show the hitbox around the enemy

    def move(self):
        if self.vel > 0: #if enemy is moving right
            if self.x  + self.vel < self.path[1]:#if he is about to move pass the move that we wanna him to change
                self.x += self.vel
            else:
                self.vel = self.vel *-1
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
        else:
            self.visible = False
        print('hit')


#here we draw everything
def redrawGameWindo():
    #global walkCount  #we maike this variable global instead of just local for this function

    #win.fill((0)) #we have to fill the background in black (0) otherwhise the rectangule still 'painted'
    win.blit(bg, (0,0)) #we put the picture bg in the position 0,0 to put the background
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) #we draw a rectangle.
    text = font.render('Score: '  + str(score), 1,  (255,0,0)) #this will render the font
    win.blit(text, (350, 10)) #we blit the font text
    man.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)


    pygame.display.update() #we need to refresh the display


#MAIN LOOP
#all pygame usually have a main loop made with a while loop.
font = pygame.font.SysFont('comicsans', 30, True) #we want to write a text with the font Comicsans, with size 30, we want bold = True

man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0 #to prevent the bullets to be shoot all at the same time
bullets = []

run = True
while run:
    #60 fps for shooting games, this is the fps, we will have 27 per second
    #pygame.time.delay(50) ##this is the time or clock to do not close to fast. Its in milisecond
    clock.tick(27) #our FPS will be 27

    #check if the goblin is hitting the Character man
    if goblin.visible == True:
        if man.hitbox[1]  < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:  # if bullet is between the y corners
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[
                2]:  # if bullet is between the x corners
                #hitSound.play()
                man.hit()
                score -= 5

    #we set up a very easy 'timer' so when we first shot a bullets its less than 3 it wont shoot, so we will have few milisecond and the shooting will works better
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    #events in pygame are things that are made by the user, moving the mouse, clikinc, typing...etc
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #to close the program, if we click the X of the window we clsoe the program
            run = False

    for bullet in bullets: #a list of bullets defined above, if they are in the screen (less than 500 and more than 0)
        #if the bullets its inside hitbox of the enemy
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:  #if bullet is between the y corners
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: #if bullet is between the x corners
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel #then our bullet will move on the x with
        else: #we want to delete our bullets if its out of the screen
            bullets.pop(bullets.index(bullet)) #pop means remove an element of the list, so its gonna find the index of the bullet and remove it from the list bullets

    keys = pygame.key.get_pressed()

    #for shooting bullets
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1 #will move left if the man is looking to the left
        else:
            facing = 1
        if len(bullets) < 5: #this is the max of the bullets that the man can shoot at the same time
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing )) #man.with//2 its gonna shoot from the middle of the man
        shootLoop = 1
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
        '''if we want to move our character up and down
        
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y += vel''' #move the character up and down
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False #TODO check if i remove this i can jump and walk
            man.left = False #TODO check if remove this i can jump and walk
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1 #if the jump reach the max level of the jump then is moving up and the y is positive
            if man.jumpCount < 0: #if the jump is after the max level, the character should go down, so the y should de increase and be negative
                neg = -1
            man.y -= (man.jumpCount ** 2)/2 * neg #we made a square function and we are gonna be slowing it down 1 by 1 (next line of code)
            man.jumpCount -= 1 #we remove the Y to the jump 1 by 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindo() #we can call also the background function at the beggining of the loop
pygame.quit()