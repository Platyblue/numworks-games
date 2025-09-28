from kandinsky import *
from ion import *
import time, math, random

col = {
    'bg': (170, 250, 100),
    'fL': (30, 150, 80),
    'fR': (200, 30, 30),
    'hat': (110, 80, 40),
    'vest': (250, 250, 0),
    'skin': (240, 220, 140),
    'bullet': (50, 50, 50),
    'score': (50, 50, 50),
    'eye': (250, 100, 100)
}
posL = [30, 80]
posR = [190, 80]
speed = 10
bullets = []
amo=[3,3]
cooldowns = [0, 0]
score = [0, 0]
end = None
game = 0

def homePage():
    global game
    fill_rect(0,0,320,225,col['score'])
    draw_string("COWBOYWORLD", 55, 10, (255, 255, 0), col['score'])
    draw_string("SIMULATOR", 175, 10, (255, 0, 255), col['score'])
    draw_string("COWBOY FIGHT", 100, 80, (200, 200, 100), col['score'])
    draw_string("COWBOY DUEL", 105, 100, (200, 200, 100), col['score'])
    draw_string("COWBOY TRAINING", 85, 120, (200, 200, 100), col['score'])
    draw_string("CHOSE GAME:", 105, 50, (250, 250, 250), col['score'])
    draw_string("<", 75, 80 + game * 20, (250, 150, 0), col['score'])
    draw_string(">", 235, 80 + game * 20, (250, 150, 0), col['score'])
    c=0
    while keydown(KEY_OK): pass
    while not keydown(KEY_OK):
        if c%12==0: draw_string("CHOSE GAME:", 105, 50, (250,250,250), col['score'])
        elif c%6==0: draw_string("CHOSE GAME:", 105, 50, (100,100,100), col['score'])
        c += 1
        if keydown(KEY_DOWN) and game<len(games)-1:
            game += 1
            fill_rect(75, 80, 10, 60, col['score'])
            fill_rect(235, 80, 10, 60, col['score'])
        elif keydown(KEY_UP) and game>0:
            game -= 1
            fill_rect(75, 80, 10, 60, col['score'])
            fill_rect(235, 80, 10, 60, col['score'])
        draw_string("<", 75, 80 + game * 20, (250, 150, 0), col['score'])
        draw_string(">", 235, 80 + game * 20, (250, 150, 0), col['score'])
        time.sleep(0.07)
    games[game]()

def animation():
    global posL, posR
    posL, posR=[104,80], [116,80]
    move('L',0)
    move('R', 0)
    for i in range(10):
        time.sleep(0.03)
        posL[0], posR[0] = posL[0]-7, posR[0]+7
        move('L', 0)
        move('R', 0)

def death(dead):
    if dead == 'L':
        for i in range(2):
            move('L', 0, 5)
            time.sleep(0.1)
        fill_rect(posL[0] - 24, posL[1], 42, 40, col['bg'])
        fill_rect(posL[0] - 40, posL[1] + 22, 9, 18, col['hat'])
        fill_rect(posL[0] - 31, posL[1] + 16, 3, 30, col['hat'])
        fill_rect(posL[0] - 28, posL[1] + 22, 6, 18, col['skin'])
        fill_rect(posL[0] - 22, posL[1] + 22, 9, 18, col['fL'])
        fill_rect(posL[0] - 13, posL[1] + 22, 13, 18, col['vest'])
        fill_rect(posL[0] - 28, posL[1] + 25, 6, 2, col['eye'])
        fill_rect(posL[0] - 26, posL[1] + 23, 2, 6, col['eye'])
    elif dead == 'R':
        for i in range(2):
            move('R', 0, -5)
            time.sleep(0.1)
        fill_rect(posR[0] - 18, posR[1], 42, 40, col['bg'])
        fill_rect(posR[0] + 40, posR[1] + 22, -9, 18, col['hat'])
        fill_rect(posR[0] + 31, posR[1] + 16, -3, 30, col['hat'])
        fill_rect(posR[0] + 28, posR[1] + 22, -6, 18, col['skin'])
        fill_rect(posR[0] + 22, posR[1] + 22, -9, 18, col['fR'])
        fill_rect(posR[0] + 13, posR[1] + 22, -13, 18, col['vest'])
        fill_rect(posR[0] + 28, posR[1] + 25, -6, 2, col['eye'])
        fill_rect(posR[0] + 26, posR[1] + 23, -2, 6, col['eye'])

def winScreen(winner):
    if winner == 'L':
        fill_rect(0, 0, 220, 225, col["fL"])
        draw_string("GG green", 80, 90, (255, 255, 255), col['fL'])
    elif winner == 'R':
        fill_rect(0, 0, 220, 225, col["fR"])
        draw_string("GG red", 80, 90, (255, 255, 255), col['fR'])
    else:
        fill_rect(0, 0, 220, 225, col["vest"])
        draw_string("DRAW", 80, 90, (0, 0, 0), col['vest'])
    while not keydown(KEY_OK):
        time.sleep(0.05)

def move(cowboy, offsetY, offsetX=0):
    if cowboy == 'L':
        fill_rect(posL[0] - 24, posL[1], 42, 40, col['bg'])
        posL[1] += offsetY
        posL[0] += offsetX
        fill_rect(posL[0] - 18, posL[1], 18, 9, col['hat'])
        fill_rect(posL[0] - 24, posL[1] + 9, 30, 3, col['hat'])
        fill_rect(posL[0] - 18, posL[1] + 12, 18, 6, col['skin'])
        fill_rect(posL[0] - 18, posL[1] + 18, 18, 9, col['fL'])
        fill_rect(posL[0] - 18, posL[1] + 27, 18, 13, col['vest'])
    else:
        fill_rect(posR[0] - 18, posR[1], 42, 40, col['bg'])
        posR[1] += offsetY
        posR[0] += offsetX
        fill_rect(posR[0], posR[1], 18, 9, col['hat'])
        fill_rect(posR[0] - 6, posR[1] + 9, 30, 3, col['hat'])
        fill_rect(posR[0], posR[1] + 12, 18, 6, col['skin'])
        fill_rect(posR[0], posR[1] + 18, 18, 9, col['fR'])
        fill_rect(posR[0], posR[1] + 27, 18, 13, col['vest'])

def FightTick():
    global cooldowns,amo
    # movements
    if keydown(KEY_SHIFT) and posL[1] > 20:
        move('L', -speed)
    elif keydown(KEY_ZERO) and posL[1] < 180:
        move('L', speed)
    if keydown(KEY_BACKSPACE) and posR[1] > 20:
        move('R', -speed)
    elif keydown(KEY_EXE) and posR[1] < 180:
        move('R', speed)
    # bullets
    for bullet in bullets: bullet.tick()
    if cooldowns[0] > 0: cooldowns[0] -= 1
    if cooldowns[1] > 0: cooldowns[1] -= 1
    if amo[0]<6: amo[0] += 0.02
    if amo[1] < 6: amo[1] += 0.02
    draw_string(str(int(amo[0])), 10, 0, col["bullet"], col["bg"])
    draw_string(str(int(amo[1])), 200, 0, col["bullet"], col["bg"])
    if keydown(KEY_SEVEN) and cooldowns[0] == 0 and amo[0]>=1: bullets.append(Bullet('L'))
    if keydown(KEY_RIGHTPARENTHESIS) and cooldowns[1] == 0 and amo[1]>=1: bullets.append(Bullet('R'))

class Bullet():
    def __init__(self, side):
        global cooldowns
        if side == 'L':
            self.pos = [posL[0] + 20, posL[1] + 19]
            self.speed = 20
            cooldowns[0] = 8
            amo[0] -= 1
            fill_rect(posL[0], posL[1] + 18, 18, 5, col['bullet'])
            fill_rect(posL[0] + 5, posL[1] + 23, 5, 5, col['bullet'])
        else:
            self.pos = [posR[0] - 27, posR[1] + 19]
            self.speed = -20
            cooldowns[1] = 8
            amo[1] -= 1
            fill_rect(posR[0], posR[1] + 18, -18, 5, col['bullet'])
            fill_rect(posR[0] - 5, posR[1] + 23, -5, 5, col['bullet'])
        fill_rect(self.pos[0], self.pos[1], 7, 3, col['bullet'])

    def tick(self):
        global end
        fill_rect(self.pos[0], self.pos[1], 7, 3, col['bg'])
        self.pos[0] += self.speed
        if 0 > self.pos[0] or self.pos[0] > 220:
            bullets.remove(self)
            return
        fill_rect(self.pos[0], self.pos[1], 7, 3, col['bullet'])
        if self.pos[0] < posL[0] and -3 < self.pos[1] - posL[1] < 40: end = "L"
        if self.pos[0] >= posR[0] and -3 < self.pos[1] - posR[1] < 40: end = "R"

def fight(kill=None):
    global end, cooldowns, posL, posR, bullets,amo
    end = None
    time.sleep(0.5)
    fill_rect(0, 0, 220, 225, col['bg'])
    fill_rect(220, 0, 100, 225, col['score'])
    draw_string("COWBOYFITE", 222, 5, (255, 255, 0), col['score'])
    draw_string("SIMULATOR", 225, 20, (255, 0, 255), col['score'])
    draw_string(str(score[0]) + ' - ' + str(score[1]), 240, 90, (255, 255, 255), col['score'])
    animation()
    posL = [30, 80]
    posR = [190, 80]
    amo = [6,6]
    bullets = []
    move("L", 0)
    move("R", 0)
    cooldowns = [15, 15]
    while not end:
        t1 = time.monotonic()
        FightTick()
        while time.monotonic() < t1 + 0.035:
            if keydown(KEY_BACK): return
            time.sleep(0.001)
    death(end)
    if end == 'L':
        score[1] += 1
    elif end == 'R':
        score[0] += 1
    if score[1]==5:
        draw_string(str(score[0]) + ' - ' + "5", 240, 90, (255, 255, 255), col['score'])
        time.sleep(1)
        winScreen('R')
    elif score[0]==5:
        draw_string("5" + ' - ' + str(score[1]), 240, 90, (255, 255, 255), col['score'])
        time.sleep(1)
        winScreen('L')
    else:
        fight()

def duel():
    posL = [30, 80]
    posR = [190, 80]
    fill_rect(0, 0, 220, 225, col['bg'])
    fill_rect(220, 0, 100, 225, col['score'])
    draw_string("COWBOYDUEL", 222, 5, (255, 255, 0), col['score'])
    draw_string("SIMULATOR", 225, 20, (255, 0, 255), col['score'])
    animation()
    draw_string("WAIT...", 75, 60, (50, 50, 50), col['bg'])
    dead = None
    shoot_time = round(time.monotonic()) + random.randint(3, 8)
    while time.monotonic()<shoot_time:
        if keydown(KEY_RIGHTPARENTHESIS):
            draw_string("RED did not wait...", 15, 60, (50, 50, 50), col['bg'])
            fill_rect(posR[0], posR[1] + 18, -18, 5, col['bullet'])
            fill_rect(posR[0] - 5, posR[1] + 23, -5, 5, col['bullet'])
            time.sleep(1)
            winScreen("L")
            return
        elif keydown(KEY_SEVEN):
            draw_string("GREEN did not wait...", 5, 60, (50, 50, 50), col['bg'])
            fill_rect(posL[0], posL[1] + 18, 18, 5, col['bullet'])
            fill_rect(posL[0] + 5, posL[1] + 23, 5, 5, col['bullet'])
            time.sleep(1)
            winScreen("R")
            return
    draw_string("SHOOT ! ", 75, 60, (200, 0, 0), col['bg'])
    while not dead:
        if keydown(KEY_RIGHTPARENTHESIS):
            dead = 'L'
            fill_rect(posR[0], posR[1] + 18, -18, 5, col['bullet'])
            fill_rect(posR[0] - 5, posR[1] + 23, -5, 5, col['bullet'])
            fill_rect(posR[0] - 18, posR[1] + 18, -7, 5, (200, 200, 0))
        if keydown(KEY_SEVEN):
            if dead == 'L': dead = 'LR'
            else: dead = 'R'
            fill_rect(posL[0], posL[1] + 18, 18, 5, col['bullet'])
            fill_rect(posL[0] + 5, posL[1] + 23, 5, 5, col['bullet'])
            fill_rect(posR[0] + 18, posR[1] + 18, 7, 5, (200, 200, 100))
    time.sleep(0.1)
    fill_rect(posR[0] + 18, posR[1] + 17, 9, 7, col['bg'])
    fill_rect(posR[0] - 18, posR[1] + 17, -9, 7, col['bg'])
    if dead == 'L':
        death(dead)
        time.sleep(0.8)
        winScreen('R')
    elif dead == 'R':
        death(dead)
        time.sleep(0.8)
        winScreen('L')
    else:
        death('R')
        death('L')
        time.sleep(0.8)
        winScreen('LR')


games=[fight, duel]
while True:
    homePage()
