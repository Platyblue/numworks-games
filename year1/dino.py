from kandinsky import *
from time import *
from ion import *
from random import *

def init():
    global black_,white_,x,y,cx,cy,bx,by,sx,sy,cactus,bird,game,score,start,jump_force,gravity,is_jumping,sneak,wing,pause,speed
    black_=(0,0,0)
    white_=(255,255,255)
    x,y=50,100
    cx,cy=310,100
    bx,by=310,100
    cactus=False
    bird=False
    game="empty"
    score=0
    start_t=0
    jump_force=13
    gravity=2
    is_jumping=False
    sneak=False
    wing=True
    pause=False
    speed=10
    sx,sy=270,30

def start_page():
  global game,score
  init()
  fill_rect(0,0,320,220,black_)
  for y in range(65):
        draw_string("OK to PLAY",110,100)
        fill_rect(0,y*4,320,4,white_)
        sleep(0.01)
  while game!="start":
    if keydown(KEY_OK):
      print("RUN!")
      game="start"
      fill_rect(0,0,320,220,black_)
      game_engine()

def dino(x,y):
  global white_,black_,sneak
  if sneak:
    fill_rect(x,y+7,15,18,black_)
    fill_rect(x+15,y+12,6,5,black_)
    fill_rect(x+15,y+18,4,3,black_)
    fill_rect(x+8,y+12,3,2,white_)
  else:
    fill_rect(x,y,15,25,black_)
    fill_rect(x+15,y+5,6,5,black_)
    fill_rect(x+15,y+11,4,3,black_)
    fill_rect(x+8,y+5,3,2,white_)

def background():
  fill_rect(0,125,340,3,black_)
  draw_string("score:"+str(score),10,10)

def gameover():
  global score
  fill_rect(0,0,320,220,black_)
  draw_string("GAME OVER",20,20)
  draw_string("score:"+str(score),20,40)
  print("game over!")
  print("score:",score)
  start_page()

def cactus_design(cx,cy):
  global black_
  fill_rect(cx+5,cy,5,25,black_)
  fill_rect(cx,cy+9,15,5,black_)
  fill_rect(cx,cy+4,3,8,black_)
  fill_rect(cx+12,cy+4,3,8,black_)

def new_cactus():
  global black_,white_,cactus,cx,cy
  cx,cy=310,100
  cactus_design(cx,cy)
  cactus=True

def cactus_update():
  global black_,white_,cactus,cx,cy,y,game,speed
  cx-=speed
  cactus_design(cx,cy)
  if not cactus and randint(1,10)==2:
    new_cactus()
  if cx<10:
    cactus=False
  if 49<cx and cx<66 and y>75:
    game="over"
    
def new_bird():
  global black_,white_,bird,bx,by,y,sneak
  bx=310
  by=95
  bird_design(bx,by)
  bird=True

def bird_update():
  global black_,white_,bird,bx,by,y,game,speed
  bx-=speed*1.5
  bird_design(bx,by)
  if not bird and score>150 and randint(1,10)==2:
    new_bird()
  if bx<10:
    bird=False
  if 49<bx and bx<66:
    if not sneak and y>95:
      game="over"
    
def bird_design(bx,by):
  global black_,score,wing
  if score%4==0:wing=True
  elif score%2==0:wing=False
  if wing:
    fill_rect(int(bx),int(by)+8,25,2,black_)
    fill_rect(int(bx)+8,int(by)+6,17,4,black_)
    fill_rect(int(bx)+13,int(by),10,7,black_)
  else:
    fill_rect(int(bx),int(by)+8,25,2,black_)
    fill_rect(int(bx)+8,int(by)+6,17,4,black_)

def get_game_dt():
  global start_t
  game_dt=monotonic()
  game_dt=game_dt-start_t
  return game_dt

def jump():
  global y,is_jumping,gravity,jump_force
  if is_jumping:
    y-=jump_force
    jump_force-=gravity
    if y>=100:
      is_jumping=False
      y=100
      jump_force=12
    
def day():
  global score,black_,white_,speed,sx,sy
  if score==250:
    speed=13
    white_=(0,0,0)
    black_=(255,255,255)
    sx,sy=270,30
    print("It's now night...Let's speed it up")
  if score>250:
    local_sx=sx-score-250
    fill_rect(local_sx+5,sy,15,20,black_)
  else:
    local_sx=sx-score
    fill_rect(local_sx,sy,20,20,black_)
    fill_rect(local_sx+2,sy+2,16,16,white_)

def end_LVL1():
  global game
  fill_rect(0,0,320,220,(255,255,255))
  draw_string("LVL 1 finished!",20,20)
  draw_string("GG try LVL2 now...",20,40)
  print("LVL 1 finished!")
  while True:
    fill_rect(x,y+7,15,18,(0,0,0))#dino
    fill_rect(x+15,y+12,6,5,(0,0,0))
    fill_rect(x+15,y+18,4,3,(0,0,0))
    fill_rect(x+8,y+12,3,2,(255,255,255))
    sleep(0.5)
    fill_rect(x,y,25,25,(255,255,255))#dino sneak
    fill_rect(x,y,15,25,(0,0,0))
    fill_rect(x+15,y+5,6,5,(0,0,0))
    fill_rect(x+15,y+11,4,3,(0,0,0))
    fill_rect(x+8,y+5,3,2,(255,255,255))
    sleep(0.5)
    fill_rect(x,y,25,25,(255,255,255))

def game_engine():
  global white_,black_,is_jumping,start_t,score,sneak,score_multiplier
  start_t=monotonic()
  score_multiplier=10
  while game!="over":
    fill_rect(0,0,320,220,white_)
    background()    
    dino(x,y)
    cactus_update()
    bird_update()
    day()
    if keydown(KEY_UP):is_jumping=True
    if keydown(KEY_DOWN):
        sneak=True
        gravity=8
    else:
        gravity=2
        sneak=False
    if is_jumping:jump()
    if keydown(KEY_SHIFT):
        score_multiplier=30
        pause=True
        sleep(0.5)
        while pause:
            if keydown(KEY_SHIFT):
                pause=False
                sleep(0.2)
    if score>500:
        end_LVL1()
        break
    sleep(0.03) 
    score=int(get_game_dt()*score_multiplier)
  if game=="over":gameover()



start_page()

  
