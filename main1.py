import pygame
import random
import math
from pygame import mixer
# initializing pygame
pygame.init()

# create the screen
screen1 = pygame.display.set_mode((1000, 600))

# Title and icon
pygame.display.set_caption('Ballon Shooter')
game_icon = pygame.image.load('assets/images/red_balloon.png')
pygame.display.set_icon(game_icon)

# Background
game_background = pygame.image.load('assets/images/game_background.png')
# Background Music
mixer.music.load('assets/music/background_music.wav')
mixer.music.play(-1)

# Shooter
Shooter = pygame.image.load('assets/images/Shooter.png')
ShooterX =10
ShooterY =1000
ShooterY_change = 10000

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',20)
textX = 10
textY = 10

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/images/crow.png'))
    enemyX.append(1000)
    enemyY.append(random.randint(0, 504))
    enemyX_change.append(1.9)
    enemyY_change.append(0)

# Balloon1
Balloon1=[]
Balloon1X= []
Balloon1Y = []
Balloon1X_change = []
Balloon1Y_change =[]
num_of_balloons=4
for i in range(num_of_balloons):
    Balloon1.append(pygame.image.load('assets/images/red_balloon.png'))
    Balloon1.append(pygame.image.load('assets/images/blue_balloon.png'))
    Balloon1X.append(927)
    Balloon1Y.append(random.randint(5, 400))
    Balloon1X_change.append(1.7)
    Balloon1Y_change.append(0)

# Bullet
Bullet = pygame.image.load('assets/images/bullet.png')
BulletX = 10
BulletY = 248
BulletX_change = 6
BulletY_change = 0
Bullet_state = "ready"

#Timer
max_time=6000
font1 = pygame.font.Font('freesansbold.ttf',20)
tX = 880
tY = 10
clock=pygame.time.Clock()

#Game Over text
game_font = pygame.font.Font('freesansbold.ttf',50)

#function to display game over
def game_over_text():
    game_text = game_font.render("GAME OVER!!!", True, (0, 0, 0))
    screen1.blit(game_text, (300,200))

#function to display winner
def you_win_text():
    win = game_font.render("LEVEL UP ", True, (0, 0, 0))
    screen1.blit(win, (300,200))

# function to display Shooter
def show_shooter(x, y):
    screen1.blit(Shooter, (x, y))


# function to display Balloon1
def show_balloon(x, y,i):
    screen1.blit(Balloon1[i], (x, y))


# function to display Bullet
def show_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen1.blit(Bullet, (x+16, y+10))

# function to display enemy
def enemy(x, y, i):
    screen1.blit(enemyImg[i], (x, y))

# function to check collision with Balloon
def isCollision(Balloon1X, Balloon1Y, BulletX, BulletY):
    distance = math.sqrt((math.pow(Balloon1X - BulletX, 2)) + (math.pow(Balloon1Y - BulletY, 2)))
    if distance < 40:
        return True
    else:
        return False

# function to check collision with enemy
def isCollision_enemy(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# function to check collision with enemy
def isCollision_shooter(enemyX, enemyY, ShooterX, ShooterY):
    distance = math.sqrt((math.pow(enemyX - ShooterX, 2)) + (math.pow(enemyY - ShooterY, 2)))
    if distance < 40:
        return True
    else:
        return False

# function to display score
def show_score(x, y):
    score = font.render("Score : "+str(score_value), True, (0, 0, 0))
    screen1.blit(score, (x, y))

# function to display time
def show_time(x, y):
    time = font1.render("Timer : "+str(max_time//60), True, (0, 0, 0))
    screen1.blit(time, (x, y))

# for closing the game screen
running = True
while running:

    # Background Color RGB
    screen1.fill((0, 0, 0))

    # Background image
    screen1.blit(game_background, (0, 0))

    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            running = False  # close game window

            # If keystroke is pressed check whether its up or down
        if game_event.type == pygame.KEYDOWN:
            if game_event.key == pygame.K_UP:
                ShooterY_change = -1
            if game_event.key == pygame.K_DOWN:
                ShooterY_change = 1
            if game_event.key == pygame.K_SPACE:  # Bullet Movement
                if Bullet_state is "ready":
                    BulletY = ShooterY
                    Bullet_sound = mixer.Sound('assets/music/gun.wav')  # Bullet sound
                    Bullet_sound.play()
                    show_bullet(BulletX, BulletY)

        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_UP or game_event.key == pygame.K_DOWN:
                ShooterY_change = 0
    if max_time>0:
        max_time -= 1
    # Collision Enemy
    for j in range(num_of_enemies):
        # Game Over
        Collision_shoot = isCollision_shooter(enemyX[j], enemyY[j], ShooterX, ShooterY)
        if Collision_shoot or max_time==0 :
            enemyX[j] = 2000
            over_sound = mixer.Sound('assets/music/gameover.wav')  # Game over sound
            over_sound.play()
            for k in range(num_of_balloons):
                Balloon1X[k] = 5000
            ShooterX=4000
        if ShooterX>1000:
            game_over_text()
            pygame.mixer.music.stop()
            break

        if score_value%50==0 and score_value !=0:
            you_win_text()
            break

    for j in range(num_of_enemies):
        # Collision with Enemy
        Collision = isCollision_enemy(enemyX[j], enemyY[j], BulletX, BulletY)
        if Collision:
            BulletX = 50
            Bullet_state = "ready"
            score_value += 4
            crow_sound = mixer.Sound('assets/music/crow_shot_music.wav')  # Crow sound
            crow_sound.play()
            enemyX[j] = 927
            enemyY[j] = random.randint(0, 504)
        enemy(enemyX[j], enemyY[j], j)
        # Enemy Entry
        if score_value >10:
            enemyX[j] -= enemyX_change[j]
            if enemyX[j] < -5:
                enemyX[j] = 930
        enemy(enemyX[j], enemyY[j], j)

    # Balloon Movement
    for i in range(num_of_balloons):
        Balloon1X[i] -= Balloon1X_change[i]
        if Balloon1X[i] <-5:
            Balloon1X[i] = 930
         # Collision Balloon
        Collision = isCollision(Balloon1X[i], Balloon1Y[i], BulletX, BulletY)
        if Collision:
            BulletX = 50
            Bullet_state = "ready"
            score_value += 2
            burst_sound = mixer.Sound('assets/music/balloon_burst_music.wav')  # burst sound
            burst_sound.play()
            Balloon1X[i] = 927
            Balloon1Y[i] = random.randint(0, 504)
        show_balloon(Balloon1X[i], Balloon1Y[i], i)

    # Shooter Movement and Boundary
    ShooterY += ShooterY_change
    if ShooterY <= 0:
        ShooterY = 0
    elif ShooterY >= 504:
        ShooterY = 504


    # Bullet Movement
    if BulletX >=950:
        BulletX = 50
        Bullet_state = "ready"

    if Bullet_state is "fire":
        show_bullet(BulletX, BulletY)  # function call
        BulletX += BulletX_change

    clock.tick(100)
    show_shooter(ShooterX, ShooterY)
    show_score(textX, textY)
    show_time(tX,tY)
    pygame.display.update()
