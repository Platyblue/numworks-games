from kandinsky import *
from time import *
from ion import *
from math import sin, cos, radians
from random import randint,choice

class Paddle:
    def __init__(self,x,player):
        self.x,self.y=x,100
        self.movement="still"
        self.player=player

    def move(self):
        if self.player=="R":
            if keydown(KEY_RIGHTPARENTHESIS) and self.y>20:
                self.y-=8
                self.movement="up"
            elif keydown(KEY_DIVISION) and self.y<185:
                self.y+=8
                self.movement="down"
            else:self.movement="still"
        else:
            if keydown(KEY_SEVEN) and self.y>20:
                self.y-=8
                self.movement="up"
            elif keydown(KEY_FOUR) and self.y<185:
                self.y+=8
                self.movement="down"
            else:self.movement="still"
    
    def update(self):
        self.move()
        fill_rect(self.x,self.y,8,25,(0,0,0))

class Ball:
    def __init__(self):
        self.velocity=10
        self.angle=choice([0,180])
        self.angle_update()
        self.x,self.y=90,115
        self.simu_x,self.simu_y=self.x,self.y
    
    def angle_update(self):
        self.vx=self.velocity*cos(radians(self.angle))#calcul each axis velocity in function of velocity and angle
        self.vy=self.velocity*sin(radians(self.angle))
    
    def move(self):
        self.simu_x+=self.vx
        self.simu_y+=self.vy
        
    def collision(self):
        global run
        if self.simu_y<20:#ceilling collided
            self.simu_y=20
            self.angle=-self.angle
            self.angle_update()
        elif self.simu_y>205:#floor collided
            self.simu_y=205
            self.angle=-self.angle
            self.angle_update()
        
        if self.simu_x>245:#right player lose
            run=False
            game.winner="gauche"
        elif self.simu_x<0:#Left player lose
            run=False
            game.winner="droite"
        
        if self.simu_x<28 and 28<self.x and self.simu_y<paddleL.y+25 and self.simu_y+5>paddleL.y: #left paddle
            self.simu_x=28
            self.angle=180-self.angle+randint(-6,6)#angle caclul +paddle movement factor +random variation
            if paddleL.movement=="up":self.angle-=30
            elif paddleL.movement=="down":self.angle+=30
            self.angle_update()
            game.score+=1
        elif self.simu_x>217 and 217>self.x and self.simu_y<paddleR.y+25 and self.simu_y+5>paddleR.y:#right paddle
            self.simu_x=217
            self.angle=180-self.angle#angle caclul +paddle movement factor
            if paddleR.movement=="up":self.angle-=30
            elif paddleR.movement=="down":self.angle+=30
            self.angle_update()
            game.score+=1

    def update(self):
        self.move()
        self.collision()
        self.x,self.y=self.simu_x,self.simu_y
        fill_rect(round(self.x),round(self.y),5,5,(0,0,0))

class Game:
    def __init__(self):
        self.score=0
        fill_rect(0,0,300,20,(0,0,0))#ceilling
        fill_rect(250,0,70,230,(0,0,0))#wall
        fill_rect(0,210,300,15,(0,0,0))#floor
        
    def update(self):
        fill_rect(0,20,250,190,(255,255,255))#clear screen
        draw_string("echanges: "+str(self.score),20,0,(255,255,255),(0,0,0))
        paddleR.update()
        paddleL.update()
        ball.update()
        sleep(0.05)
  
while True:
    sleep(0.5) 
    ok=False
    run=True
    game=Game()
    ball=Ball()
    paddleL=Paddle(20,"L")
    paddleR=Paddle(222,"R")
    while run: #run the game
        game.update()
    fill_rect(0,0,320,225,(0,0,0)) #death screen
    draw_string("Victoire "+game.winner+", Press OK",40,80,(255,200,0),(0,0,0))
    draw_string("nombre d'echanges: "+str(game.score),60,110,(255,200,0),(0,0,0))
    while not ok:
        if keydown(KEY_OK): ok=True#restart the game on keydown