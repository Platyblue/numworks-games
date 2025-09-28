from ion import *
from time import *
from kandinsky import *
from random import *

color = {
    "ship": (0, 240, 0),
    "bg": (0, 0, 0),
    "shipProjectile": (0, 148, 0),
    "invader":(248,252,248),
    "invaderProjectile":(200,200,200),
    "bunker": (0,252,0),
    "UFO": (248,200,96),
    "infoPanel": (0,0,0)
}
last_ufo=0
speed=3
invaders=[]
rightest_invader=-1
leftest_invader=0
bottom_invaders=[]
invader_projectiles=[]
ship_projectiles=[]
bunkers=[]

class Ship:
    def __init__(self):
        self.width = 18
        self.x, self.y = 160 - self.width // 2, 200
        self.render()

    def update(self):
        fill_rect(self.x, self.y, self.width, 5, color["bg"])
        fill_rect(self.x + 6, self.y, 6, -2, color["bg"])
        if keydown(KEY_LEFT) and self.x>5:
            self.x -= 6
        if keydown(KEY_RIGHT) and self.x<315:
            self.x += 6
        self.render()

    def render(self):
        global color
        fill_rect(self.x, self.y, self.width,5, color["ship"])
        fill_rect(self.x+6,self.y,6,-2, color["ship"])

class ShipProjectile:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def missileCollision(self,x,y):
        if x-2<self.x<x+2 and y<self.y<y+21: ship_projectiles.remove(self)

    def update(self):
        global color,invaders,ship_projectiles,ufo,score
        fill_rect(self.x, self.y, 2, 8, color["bg"])
        self.y -= 10
        if self.y < 20:
            ship_projectiles.remove(self)
            return
        for i in range(0,10): # check if invader touch
            if get_pixel(self.x,self.y+i)==color["invader"] or get_pixel(self.x+1,self.y+i)==color["invader"]:
                ship_projectiles.remove(self)
                for invader in invaders:
                    invader.killedTrigger(self.x,self.y+i)
                return
            if get_pixel(self.x,self.y+i)==color["UFO"] or get_pixel(self.x+1,self.y+i)==color["UFO"]:
                ship_projectiles.remove(self)           # check if ufo shot
                fill_rect(ufo.x, ufo.y, 20, 8, color["bg"])
                score+=choice([200,250,300])
                infoPanel()
                ufo=0
        if self.y>150:      #check if touch bunker
            for i in range(1, 4):
                if get_pixel(self.x,self.y-i*4)==color["bunker"] or get_pixel(self.x+1,self.y-i*4)==color["bunker"]:
                    ship_projectiles.remove(self)
                    for bunker in bunkers: bunker.damage(self.x, self.y-i*4)
                    return
        self.render()

    def render(self):
        global color
        fill_rect(self.x, self.y, 2, 8, color["shipProjectile"])

class Invader:
    def __init__(self,x,y,type):
        self.x,self.y=x,y
        self.type=type

    def move(self):
        global speed,color
        self.x+=speed
        self.render()

    def killedTrigger(self,x,y):       #trigger when an invader is touched
        global bottom_invaders,score
        if self.x-3<x<self.x+14 and self.y-3<y<self.y+12:
            score+=self.type*10
            infoPanel()
            for i,index_invader in enumerate(bottom_invaders):
                if index_invader>invaders.index(self): bottom_invaders[i]-=1
                elif index_invader==invaders.index(self): bottom_invaders[i]=0
                fill_rect(self.x, self.y, 11, 8, color["bg"])
            invaders.remove(self)
            if not invaders:newWave()
            getSideInvaders()
            getBottomInvaders()

    def render(self):
        global color
        fill_rect(self.x, self.y, 11, 8, color["invader"])
        #if self.type==1:

class InvaderProjectile:
    def __init__(self,x,y,speed):
        self.x, self.y = x, y+8
        self.speed=speed

    def update(self):
        global invader_projectiles, ship_projectiles, color, bunkers
        fill_rect(self.x, self.y, 2, 8, color["bg"])
        self.y+=self.speed
        if self.y>220:
            invader_projectiles.remove(self)
            return
        if 208>self.y>192 and ship.x<self.x<ship.x+ship.width: shipShot()
        for i in range(5):
            if get_pixel(self.x-2,self.y+i*4)==color["shipProjectile"] or get_pixel(self.x,self.y+i*4)==color["shipProjectile"] or get_pixel(self.x+2,self.y+i*5)==color["shipProjectile"]:
                invader_projectiles.remove(self)
                for projectile in ship_projectiles: projectile.missileCollision(self.x, self.y)
                return
        for i in range(1,4):
            if get_pixel(self.x,self.y+i*4)==color["bunker"] or get_pixel(self.x+1,self.y+i*4)==color["bunker"]:
                try:invader_projectiles.remove(self)
                except:print("problem")
                for bunker in bunkers: bunker.damage(self.x,self.y+i*4)
                return
        self.render()

    def render(self):
        global color
        fill_rect(self.x, self.y, 2,8, color["invaderProjectile"])

class Bunker:
    def __init__(self,x):
        self.x, self.y=x, 175
        self.bunker=[
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 1],
        ]
        self.render()

    def damage(self,x,y):
        for px_y in range(4):
            for px_x in range(7):
                if y>=px_y*4+self.y>=y-4 and x>=px_x*4+self.x>=x-4:
                    self.bunker[px_y][px_x]=0
                    self.render()
                    return

    def render(self):
        global color
        for y,pixels in enumerate(self.bunker):
            for x,pixel in enumerate(pixels):
                if pixel==1: fill_rect(self.x+x*4, self.y+y*4,4,4,color["bunker"])
                elif pixel==0: fill_rect(self.x+x*4, self.y+y*4,4,4,color["bg"])

class UFO:
    def __init__(self):
        self.x, self.y = 320, 20
        self.render()

    def update(self):
        global ufo, color
        fill_rect(self.x, self.y, 20, 8, color["bg"])
        self.x-=5
        if self.x<-10:ufo=0
        else:self.render()

    def render(self):
        global color
        fill_rect(self.x, self.y, 20, 8, color["UFO"])

def newWave():
    global color,ship,ufo,last_ufo,ship_projectiles,rightest_invader,leftest_invader,invaders,invader_projectiles,bunkers,bottom_invaders
    fill_rect(0, 16, 320, 209, color["bg"])
    ship = Ship()
    sleep(0.5)
    ship_projectiles = []
    rightest_invader = -1
    leftest_invader = 0
    invaders = []
    invader_projectiles = []
    ufo=0
    last_ufo=0
    for x in range(1, 10): invaders.append(Invader(20 * x, 20, 3))  # summon the worst invaders(type 3)
    for y in range(2, 4):
        for x in range(1, 10): invaders.append(Invader(20 * x, 20 * y, 2))  # summon the basics invaders(type 2)
    for x in range(1, 10): invaders.append(Invader(20 * x, 80, 1))  # summon the innofensives invaders(type 1)
    bottom_invaders=[27,28,29,30,31,32,33,34,35]
    bunkers = [Bunker(34), Bunker(90), Bunker(146), Bunker(202), Bunker(258)]

def getSideInvaders():  #get the rightest and leftest invaders index
    global invaders, leftest_invader, rightest_invader
    max_right=0
    max_left=320
    for invader in invaders:
        if invader.x>max_right:
            rightest_invader=invaders.index(invader)
            max_right=invader.x
        if invader.x<max_left:
            leftest_invader=invaders.index(invader)
            max_left=invader.x

def getBottomInvaders():
    global invaders,bottom_invaders,leftest_invader
    posx=invaders[leftest_invader].x
    for invader in invaders:
        for i in range(9):
            if invader.x == posx + 20*i and invaders[bottom_invaders[i]].y < invader.y:
                bottom_invaders[i]=invaders.index(invader)
                break

def gameOver():
    global run
    run=False
    print("GAME OVER")

def shipShot():
    global lives, color
    if lives==1:gameOver()
    else:
        lives-=1
        fill_rect(200,4,66,7,color["infoPanel"])
        infoPanel()
        fill_rect(ship.x, ship.y-2, 18, 7, color["bg"])
        ship.x, ship.y = 151, 200
        for i in range(3):
            fill_rect(ship.x, ship.y-2, 18, 7, color["bg"])
            sleep(0.2)
            fill_rect(ship.x, ship.y, 18, 5, color["ship"])
            fill_rect(ship.x + 6, ship.y, 6, -2, color["ship"])
            sleep(0.2)

def infoPanel():
    global color,score,lives
    draw_string("score: "+str(score),5,-3,(255,255,255),color["infoPanel"])
    draw_string("lives:", 135, -3, (255, 255, 255), color["infoPanel"])
    for i in range(lives):
        fill_rect(200+i*22,6,18, 5,(255,255,255))
        fill_rect(206+i*22,6,6,-2,(255,255,255))

def gameEngine():
    global lives,color,score,speed,invaders,rightest_invader,leftest_invader,invader_projectiles,bottom_invaders,ufo,last_ufo,ship,run,ship_projectiles,bunkers, invader_projectiles
    run = True
    score=0
    lives=3
    key_up=False
    cooldown=10
    invader_move_in = 15
    invader_move_time = 40
    speed=12
    fill_rect(0, 0, 320, 15, color["infoPanel"])
    infoPanel()
    ufo=0
    last_ufo = 0
    next_ufo = randint(200, 400)
    newWave()
    start_time=round(monotonic())
    updates=0.0

    while run:
        if keydown(KEY_RIGHT) or keydown(KEY_LEFT):ship.update()

        #invaders-----------------
        if len(invaders)%4==0: invader_move_time=len(invaders)//4+3  #accelerate every 4invaders killed
        invader_move_in-=1
        if invader_move_in==0:
            for invader in invaders: fill_rect(invader.x, invader.y, 11, 8, color["bg"])
            invader_move_in=invader_move_time
            if invaders[rightest_invader].x>290 or invaders[leftest_invader].x<20:     #if wall reached: turn,go down
                speed=-speed
                for invader in invaders:
                    if invader.y>160: gameOver()   #when invaders reach bottom
                    invader.y+=10
                    invader.move()
            else:
                for invader in invaders:invader.move()
            try:
                index_i=bottom_invaders[choice([0,1,2,3,4,5,6,7,8,9])] #make a random bottom invader shoot projectile
                if invaders[index_i].type==2:invader_projectiles.append(InvaderProjectile(invaders[index_i].x+5, invaders[index_i].y, 7))
                elif invaders[index_i].type == 3: invader_projectiles.append(InvaderProjectile(invaders[index_i].x + 5, invaders[index_i].y, 10))
            except:pass

        # UFO-----------------------
        if ufo!=0: ufo.update()
        elif last_ufo==next_ufo:
            next_ufo=randint(200,400)
            last_ufo=0
            ufo=UFO()
        else:last_ufo+=1

        # ship projectiles----------
        if cooldown < 6: cooldown += 1
        if key_up and not keydown(KEY_OK): key_up=False         # force player to press key every time rather than keeping it pressed
        if keydown(KEY_OK) and key_up==False and cooldown > 5:  # summon missile on key up
            ship_projectiles.append(ShipProjectile(ship.x + ship.width // 2 - 1, ship.y+4))
            cooldown = 0
            key_up=True
        for i, projectile in enumerate(ship_projectiles):
            projectile.update()
        if key_up:ship.render()

        # invaders projectiles---------------
        for projectile in invader_projectiles: projectile.update()

        updates+=0.05
        while monotonic()<updates+start_time:sleep(0.01)

fill_rect(0,0,320,225,(0,0,0))
draw_string("SPACE INVADERS",90,80,(255,255,255),color["bg"])
draw_string("OK TO PLAY",110,100,(255,255,255),color["bg"])
while True:
    while not keydown(KEY_OK): sleep(0.1)
    gameEngine()
    fill_rect(0, 0, 320, 225, (0, 0, 0))
    draw_string("SPACE INVADERS", 90, 80, (255, 255, 255), color["bg"])
    draw_string("SCORE: "+str(score),110,100,(255,255,255),color["bg"])
