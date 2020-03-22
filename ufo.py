from microbit import *
import random

BULLET_SPEED = 3
PLAYER_SPEED = 2
UFO_SPEED = 15
game_go = True
score = 0

class Player:
    def __init__(self):
        self.x = 2
        self.y = 4
        display.set_pixel(self.x, self.y, 9)

    def move(self, dx):
        display.set_pixel(self.x, 4, 0)
        self.x += dx
        self.x = min(max(self.x, 0), 4)
        display.set_pixel(self.x, 4, 9)

class Bullet:
    def __init__(self):
        self.y = 0
        self.x = 0
        self.count = 0
 
    def start(self, px):
        self.x = px
        self.y = 3
        self.count += 1
        display.set_pixel(self.x, self.y, 9)
    
    def move(self):
        global score, game_go, UFO_SPEED ,u
        if self.count > 0:
            display.set_pixel(self.x, self.y, 0)
            if self.y != 0:
                self.y -= 1
                if self.x == u.x and self.y == u.y:
                    score += 1
                    UFO_SPEED -= 1
                    if UFO_SPEED <= 3:
                        game_go = False
                        return
                    sleep(100)
                    u.start()
                display.set_pixel(self.x, self.y, 9)
            else:
                self.count = 0

class Ufo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.count = 0
        self.moveRight = True
        self.moveCount = 0
    
    def start(self):
        self.x = random.randint(1, 3) 
        self.y = 0
        self.count = 1
        display.set_pixel(self.x, self.y, 9)

    def delete(self):
        self.count = 0
        display.set_pixel(self.x, self.y, 0)
    
    def move(self):
        global game_go
        if self.count > 0:
            self.moveCount += 1
            display.set_pixel(self.x, self.y, 0)
            if random.randint(0, 3) == 3 or self.x == 0 or self.x == 4:
                self.moveRight = not self.moveRight
            if self.moveCount >= 6:
                if self.y == 3:
                    game_go = False
                    return
                else:
                    self.y += 1
                self.moveCount = 0
            else:
                if self.moveRight:
                    self.x += 1
                else:
                    self.x -= 1
            self.x = min(max(self.x, 0), 4)
            display.set_pixel(self.x, self.y, 9)

def player_go():
    global p
    ax = accelerometer.get_x()
    if ax > 300:
        p.move(1)
    elif ax < -300:
        p.move(-1)

display.scroll('UFO')
bcount = BULLET_SPEED
pcount = PLAYER_SPEED
ucount = UFO_SPEED

display.clear()
b = Bullet()  
p = Player()
u = Ufo()
u.start()

while game_go:
    time_start = running_time()

    if button_a.is_pressed():
        if b.count == 0:
            b.start(p.x)
    if bcount == 0:
        b.move()
        bcount = BULLET_SPEED
    else:
        bcount -= 1
    if pcount == 0:
        player_go()
        pcount = PLAYER_SPEED
    else:
        pcount -= 1
    if ucount == 0:
        u.move()
        ucount = UFO_SPEED
    else:
        ucount -= 1

    time_taken = running_time() - time_start
    wait = 40
    if time_taken < wait:
        sleep(wait - time_taken)

display.scroll('SCORE:' + str(score), loop=True)