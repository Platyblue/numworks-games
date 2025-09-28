from kandinsky import *
from ion import *
from time import *
from math import radians,sin,cos
from random import choice,randint,random

hi=131

color={
    "bg":(30,30,30),
    "red":(248,48,48),
    "blue":(48,48,248),
    "white":(250,250,250),
    "vanished":(31,31,31),
}

r=27
center = [170, 107]
updates = 0

do_quote=False
quote_y=20
quotes=[
        "Take the bet that love exist, and do a loving act",
        "If you are in trouble: Better call Saul",
        "C'est en forgeant qu'on devient forgeron",
        "Un jour tu seras le meilleur joueur",
        "Il faut penser de maniere circulaire",
        "Certaines choses meritent qu'on se batte pour elles",
        "Un ninja n'abandonne jamais",
        "Aiguise la lame de ton avenir",
        "Il faut parfois savoir tourner la page",
        "Fait face a ton destin",
        "  Affronte tes peurs",
        "  N'abandonne que.",
        "MudaMudaMudaMudaMuda  Zawarudo",
        "Pierre qui roule n'amasse pas mousse",
        "  42",
        "Un grand pouvoir implique de grandes responsabilites",
        " Je suis qui je suis",
        "Toujours plus vite,  toujours plus haut,  toujours plus fort",
        "  Droit au but",
        "It's all good man.",
        "You don't get to live a bad life & have good things happen 2u",
        "You, sir, are a fish.",
        "You are the one who knocks",
        "You are not in danger, you are the danger",
        "Well, A Stranger Is Just A Friend You Ain't Met Yet.",
        "Ne remet jamais a plus tard ce que tu peux faire maintenant",
        "Une route est quelque chose qu l'on construis toi-meme",
        ]

def ball_update():
    global r,angle,center,speed,x1,x2,y1,y2
    fill_rect(x1, y1, 6, 6, color["bg"])
    fill_rect(x2, y2, 6, 6, color["bg"])
    # add controls
    if keydown(KEY_LEFT) or keydown(KEY_SHIFT): speed=16
    elif keydown(KEY_RIGHT) or keydown(KEY_BACKSPACE): speed=-16
    else: speed=0
    angle+=speed
    # make angle stay between 0 and 360
    if angle>360: angle-=360
    elif angle<0: angle+=360
    # equation to get balls pos from the angle
    y1=round(r*cos(radians(angle))) + center[0]
    x1=round(r*sin(radians(angle))) + center[1]
    y2 = round(r * cos(radians(angle+180))) + center[0]
    x2 = round(r * sin(radians(angle+180))) + center[1]
    # show balls
    fill_rect(x1,y1,6,6,color["red"])
    fill_rect(x2, y2, 6, 6,color["blue"])

class Obstacle:
    def __init__(self):
        global last_obstacle,score
        # types; 0=LeftLine, 1=RightLine, 2=rectangle, 3=RightLine+LeftLine
        types=[0,1,2,3]
        speeds=[6]
        if last_obstacle==2: types.remove(2)
        elif last_obstacle == 3 or score<10: types.remove(3)
        self.type = choice(types)
        last_obstacle=self.type
        # add 1/3 chance to spawn vanishing obstacle after some time
        if (score>15 and score<30 and randint(0,3)==1) or (score>30 and random()): self.vanishing=True
        else: self.vanishing=False
        self.light=239
        # data = [y, x, width, height]
        if self.type==0: self.data=[0,0,115,6]
        elif self.type==1: self.data=[0,105,115,6]
        elif self.type==2: self.data=[0,95,30,10]
        elif self.type==3: self.data=[0,0,85,6]
        if score > 15: speeds.append(8)
        if score > 30: speeds.append(10)
        if score > 45: speeds.append(12)
        self.speed=choice(speeds)
        self.data[0] = 138 - self.speed*23
        self.mark= 0

    def update(self):
        global score
        fill_rect(self.data[1], self.data[0], self.data[2], self.data[3], color["bg"])
        fill_rect(0, self.mark, 6, 3, color["bg"])
        if self.type == 3: fill_rect(135, self.data[0], 85, self.data[3], color["bg"])
        # add speed difference
        if self.data[0]<138: self.data[0]+=self.speed
        else: self.data[0]+=6
        self.mark+=6
        if self.data[0]>225:
            obstacles.remove(self)
            score+=1
        else: self.render()

    def render(self):
        if self.vanishing:
            if self.data[0]<120 and self.data[0]>20:
                self.light -= 13
                fill_rect(self.data[1],self.data[0],self.data[2], self.data[3],(self.light,self.light,self.light))
                if self.type == 3: fill_rect(140, self.data[0], 80, self.data[3], (self.light,self.light,self.light))
            else:
                fill_rect(self.data[1],self.data[0],self.data[2], self.data[3],color["vanished"])
                if self.type == 3: fill_rect(140, self.data[0], 80, self.data[3], color["vanished"])
        else:
            fill_rect(self.data[1],self.data[0],self.data[2], self.data[3],color["white"])
            if self.type == 3: fill_rect(140, self.data[0], 80, self.data[3], color["white"])
        fill_rect(0, self.mark, 6, 3, color["white"])

def collision():
    global x1,x2,y1,y2
    if get_pixel(x1,y1)!=color["red"] or get_pixel(x1+5,y1)!=color["red"] or get_pixel(x1+5,y1+5)!=color["red"] \
            or get_pixel(x1,y1+5)!=color["red"] or get_pixel(x2,y2)!=color["blue"] or get_pixel(x2+5,y2)!=color["blue"] \
            or get_pixel(x2+5,y2+5)!=color["blue"] or get_pixel(x2,y2+5)!=color["blue"]: return True

def quote():
    global quote_y,do_quote
    fill_rect(0, quote_y-6, 220, 60, color["bg"])
    for i,letter in enumerate(quotation):
        #if i==21: draw_string("-", 0, quote_y+20, color["white"], color["bg"])
        #if i == 42: draw_string("-", 0, quote_y+40, color["white"], color["bg"])
        if i<22: draw_string(letter, 10*i, quote_y, color["white"], color["bg"])
        elif i<44: draw_string(letter, 10*(i-22), quote_y+20, color["white"], color["bg"])
        else: draw_string(letter, 10*(i-44), quote_y+40, color["white"], color["bg"])
    quote_y+=6
    if quote_y>80:
        fill_rect(0, quote_y-6, 220, 60, color["bg"])
        do_quote=False
        quote_y=20

def main():
    global score,updates,run,tpf,start_time
    while run:
        if do_quote: quote()
        draw_string(str(score), 260, 80, (0, 0, 0), (250, 180, 50))
        draw_string(str(round((0.1-tpf)*2000))+"%", 250, 120, (0, 0, 0), (250, 180, 50))
        ball_update()
        if updates%11==0: obstacles.append(Obstacle()) # spawn obstacle each 0.5s
        if updates%11==0 and tpf>0.05:
            tpf-=0.001
        for obstacle in obstacles: obstacle.update()
        if collision():
            run = False
            sleep(0.1)
        # fps regulator
        while start_time + updates*tpf > monotonic(): sleep(0.001)
        start_time = monotonic() - updates*tpf
        updates+=1

#start screen
fill_rect(0,0,220,225,color["bg"])
fill_rect(220,0,100,225,(250, 180, 50))
draw_string("PLAY CIRCLES",50,100,color["white"],color["bg"])
while not keydown(KEY_OK):
    if updates>10: draw_string("press OK", 70, 120, color["white"], color["bg"])
    else: draw_string("press OK", 70, 120, (120,120,120), color["bg"])
    sleep(0.05)
    updates+=1
    if updates>21: updates=0
updates=0
fill_rect(0,0,220,225,color["bg"])
draw_string("HI SCORE", 225, 20, (0, 0, 200), (250, 180, 50))
draw_string(str(hi),255,40,(0,0,200),(250,180,50))
draw_string("SCORE:", 240, 60, (0, 0, 0), (250, 180, 50))
draw_string("SPEED:", 240, 100, (0, 0, 0), (250, 180, 50))

while True:
    last_obstacle = 0
    tpf = 0.076
    score = 0
    angle = 90
    speed = 0
    x1, x2, y1, y2 = 107, 107, 170, 143
    run = True
    #add random quote
    do_quote=True
    quotation=choice(quotes)
    quote()
    obstacles = []
    ball_update()
    sleep(0.5)
    if len(quotation)>22\
            : sleep(0.5)
    if len(quotation) > 44: sleep(0.5)
    start_time = monotonic()
    main()
    # restart screen
    fill_rect(10, 0, 210, 225, color["bg"])
    fill_rect(220, 0, 100, 225, (250, 180, 50))
    draw_string("SCORE: "+str(score), 75-len(str(score))*5, 80, color["white"], color["bg"])
    while not keydown(KEY_OK):
        if updates > 10:
            draw_string("press OK", 70, 120, color["white"], color["bg"])
        else:
            draw_string("press OK", 70, 120, (120, 120, 120), color["bg"])
        sleep(0.05)
        updates += 1
        if updates > 21: updates = 0
    updates = 0
    fill_rect(0, 0, 220, 225, color["bg"])
    draw_string("SCORE:", 240, 60, (0, 0, 0), (250, 180, 50))
    draw_string("SPEED:", 240, 100, (0, 0, 0), (250, 180, 50))
    draw_string("HI SCORE", 225, 20, (0, 0, 200), (250, 180, 50))
    draw_string(str(hi),255,40,(0,0,200),(250,180,50))
