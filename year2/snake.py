from time import *
from kandinsky import *
from ion import *
from random import *

tm=0.1
col = {
    "snake":(0,250,0),
    "apple":(250,0,0),
    "bg":(180,250,150),
    "screen":(0,0,0)
}

def main():
    global x,y,dir,pompos,score
    fill_rect(x, y, 10, 10, (col["snake"]))
    if keydown(KEY_UP) and not dir==3: dir=1
    elif keydown(KEY_DOWN) and dir!=1: dir=3
    elif keydown(KEY_LEFT) and dir!=2: dir=4
    elif keydown(KEY_RIGHT) and dir!=4: dir=2
    if dir==1: y-=10
    elif dir==2: x+=10
    elif dir==3: y+=10
    elif dir==4: x-=10

    if x>200 or y>200 or x<10 or y<10 or (x,y) in body:
        end()
        return
    body.append((x,y))
    # test
    if x!=pompos[0] or y!=pompos[1]:
        fill_rect(body[0][0], body[0][1], 10, 10,col["bg"])
        del body[0]
    else:
        pomme()
        score+=1
        draw_string('score:'+str(score),220,70,(255,255,255),(0,0,0))
    fill_rect(x, y, 10, 10, (col["snake"]))
    if dir==3 or dir==1:
        fill_rect(x,y+3,4,3,(250,250,250))
        fill_rect(x+6, y + 3, 4, 3, (250, 250, 250))
        fill_rect(x,y+3,2,2,(0,0,0))
        fill_rect(x+8, y + 3, 2, 2, (0, 0, 0))
    else:
        fill_rect(x+3,y,3,4,(250,250,250))
        fill_rect(x+3,y+6, 3, 4, (250, 250, 250))
        fill_rect(x + 3, y, 2, 2, (0, 0, 0))
        fill_rect(x + 3, y + 8, 2, 2, (0, 0, 0))
    if dir==1:
        fill_rect(x+2,y,6,2,(250,100,100))
    elif dir==2:
        fill_rect(x+8,y+2,2,6,(250,100,100))
    elif dir == 3:
        fill_rect(x +2, y + 8, 6, 2, (250, 100, 100))
    elif dir == 4:
        fill_rect(x , y + 2, 2, 6, (250, 100, 100))
def pomme():
    global pompos
    x=randint(1,20)*10
    y=randint(1,20)*10
    while (x,y) in body:
        x = randint(1, 20) * 10
        y = randint(1, 20) * 10
    pompos=(x,y)
    fill_rect(x, y, 10, 10, col["apple"])

def end():
    global gameover
    gameover=True
    draw_string('Game over :)',50,70,(255,255,255),(0,0,0))
    draw_string('Press OK bitch', 40, 110, (255, 255, 255), (0, 0, 0))

while True:
    score=0
    gameover=False
    pompos=(100,100)
    x=50
    y=50
    dir=2
    body=[(x-10,y-10),(x,y)]
    fill_rect(0,0,320,225,col["screen"])
    fill_rect(10,10,200,200,col["bg"])
    draw_string('score:' + '0', 220, 70, (255, 255, 255), (0, 0, 0))
    pomme()
    while gameover==False:
        main()
        sleep(tm)
    while not keydown(KEY_OK):
        sleep(0.1)
